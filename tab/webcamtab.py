from pyqt.profile.tab.packages.webcam import WebCam

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap

class WebCamTab(QWidget):
    def __init__(self):
        super(WebCamTab, self).__init__()

    def generateWebCamTab(self):
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
        # TODO: lambda를 사용해야만 인식하는 이유 알아야 함.
        self.playBtn.clicked.connect(lambda : self._startWebCam())

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