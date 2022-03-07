from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

import sys
import cv2
import logging
import time
from dataclasses import dataclass
import tab


loggingFormat = "%(asctime)s: %(message)s"
logging.basicConfig(format=loggingFormat, level=logging.INFO, datefmt="%H:%M:%S")

@dataclass
class TabInfo:
    """
    tab 제목을 위한 struct
    """
    tab1 = "KimJunHee Resume"
    tab2 = "video"

@dataclass
class WindowSize:
    """
    Window size 설정을 위한 struct
    """
    default_width = 700     # 기본 넓이
    default_height = 700    # 기본 높이
    minimum_width = 500     # 최소 넓이
    minimum_height = 500    # 최소 높이
    maximum_width = 900     # 최대 넓이
    maximum_height = 900    # 최대 높이

class MyApp(QMainWindow):

    def __init__(self):
        """
        MyApp 생성자
        """
        super().__init__()
        self._setWindowConfiguration()
        self.show()

    def _makeCenterWindow(self):
        """
        window 화면을 중앙에 띄움
        :return: None
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _setWindowConfiguration(self):
        """
        window 구성 설정
        :return: None
        """
        self.resize(WindowSize.default_width, WindowSize.default_height)
        self.setMinimumSize(WindowSize.minimum_width, WindowSize.minimum_height)
        # TODO:  window 최대화 문제 있음
        self.setMaximumSize(WindowSize.maximum_width, WindowSize.maximum_height)
        self.setWindowTitle("KimJunHee's portfolio")
        self._makeCenterWindow()

        # layout에 widget을 설정
        wg = MyWidget()
        self.setCentralWidget(wg)


class MyWidget(QWidget):
    def __init__(self):
        """
        MyWidget 생성자
        """
        super().__init__()
        self.running = False
        self._my_homepage_url = "https://kimjunheekor.github.io/about/"
        self._TabInfo = TabInfo()
        self._initUI()

    def _initUI(self):
        """
        초기화된 화면을 보여주는 UI
        :return: None
        """
        # 위젯 설정
        tabs = QTabWidget()
        tabs.addTab(self._resumeTab(), self._TabInfo.tab1)
        tabs.addTab(self._webCamTab(), self._TabInfo.tab2)
        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        # 레이아웃 설정
        self.setLayout(vbox)

        # 윈도우 설정
        self.show()

    def _resumeTab(self):
        """
        Resume 홈페이지 연결한 후 Qwidget에 display
        :return: tab(QWidget)
        """
        # browser 생성
        browser = QWebEngineView()
        browser.setUrl(QUrl(self._my_homepage_url))

        # BoxLayout 생성 후 browser 연결
        vbox = QVBoxLayout()
        vbox.addWidget(browser)

        # tabWidget 생성 후 QVBoxLayout 연결
        tab = QWidget()
        tab.setLayout(vbox)

        return tab

    def _webCamTab(self):
        """
        webcam tab 구현
        :return: tab(QWidget)
        """
        # Layout 설정
        vbox = QVBoxLayout()

        # webcam 위젯 설정
        self.webcamWidget = QLabel()
        self.webcamWidget.setText("WebCam")
        self.webcam = None

        # 웹캠 시작 버튼
        self.playBtn = QPushButton()
        self.playBtn.setText("Start")
        self.playBtn.clicked.connect(self._startWebCam)

        # 웹캠 정지버튼
        stopBtn = QPushButton()
        stopBtn.setText("Quit")
        stopBtn.clicked.connect(self._quitWebCam)

        # BoxLayout 생성 후 browser 연결

        vbox.addWidget(self.webcamWidget)
        vbox.addWidget(self.playBtn)
        vbox.addWidget(stopBtn)

        # tabWidget 생성 후 QVBoxLayout 연결
        tab = QWidget()
        tab.setLayout(vbox)

        return tab

    def _startWebCam(self):
        """
        webcam start
        :return: None
        """
        if self.webcam is None:
            self.webcam = WebCam()

        if not self.webcam.isRunning():
            self.webcam.start()
            self.webcam.activeRunWebCam()

        if self.playBtn.text() == "Start":
            self.webcam.threadActive = True
            self.webcam.imageUpdate.connect(self._imageUpdateSlot)
            self.playBtn.setText("Abort")
        elif self.playBtn.text() == "Abort":
            self._abortWebCam()
            self.playBtn.setText("Resume")
        else:
            self._resumeWebCam()
            self.playBtn.setText("Abort")


    def _imageUpdateSlot(self, QImage):
        """
        PyQT5 slot for webcam image update
        :param QImage: QImage
        :return: None
        """
        width = self.webcamWidget.width()
        height = self.webcamWidget.height()
        image = QPixmap.fromImage(QImage).scaled(width, height)
        self.webcamWidget.setPixmap(image)

    def _abortWebCam(self):
        """
        Abort webcam
        :return: None
        """
        self.webcam.deactiveRunWebCam()

    def _resumeWebCam(self):
        """
        resum webcam
        :return: None
        """
        self.webcam.activeRunWebCam()

    def _quitWebCam(self):
        """
        quit webcam
        :return: None
        """
        if self.webcam is None:
            return None
        self.webcam.quitWebCam()
        self.webcam.imageUpdate.disconnect(self._imageUpdateSlot)
        self.webcam.quit()
        self.webcam = None

        self.webcamWidget.clear()
        self.webcamWidget.setText("WebCam")
        self.playBtn.setText("Start")


class WebCam(QThread):
    """
    webcam 연결 class
    """
    imageUpdate = pyqtSignal(QImage)
    threadActive = True
    capture = None

    def run(self):
        """
        WebCam Thread run
        @params: None
        :return: None
        """
        while self.threadActive:
            if self.capture is None:
                try:
                    self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                except Exception as e:
                    logging.critical(f"Critical ERROR : {e}")

            ret, frame = self.capture.read()

            if ret:
                self._faceDetection(frame)
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flippedImage = cv2.flip(image, 1)
                convert_to_Qtform = QImage(flippedImage.data,
                                           flippedImage.shape[1],
                                           flippedImage.shape[0],
                                           QImage.Format_RGB888)
                picture = convert_to_Qtform.scaled(WindowSize.maximum_width, # width
                                                   WindowSize.maximum_height, # height
                                                   Qt.KeepAspectRatio)

                self.imageUpdate.emit(picture)

    def activeRunWebCam(self):
        """
        WebCam running is active
        @params: None
        :return: None
        """
        self.threadActive = True

    def deactiveRunWebCam(self):
        """
        WebCam running is deactive
        @params: None
        :return: None
        """
        self.threadActive = False

    def quitWebCam(self):
        """
        Quit the WebCam running
        @params:None
        :return: None
        """
        self.threadActive = False

        if self.capture is None:
            return

        if self.capture.isOpened():
            self.capture.release()
            self.wait(1500)
            del self.capture

    def _faceDetection(self, Image):
        """
        Detect faces at input image, then draw rectangle at face boundary in the input image
        :param Image: Image
        :return: Image
        """
        face_cascade = cv2.CascadeClassifier("face/haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(image=Image, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(Image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        return Image



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())