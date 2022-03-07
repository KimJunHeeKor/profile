from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

import sys
# import logging
from data.dataclass import *
from tab.webcamtab import WebCamTab
from tab.resume import ResumeTab

# loggingFormat = "%(asctime)s: %(message)s"
# logging.basicConfig(format=loggingFormat, level=logging.INFO, datefmt="%H:%M:%S")

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
        self._TabInfo = TabInfo()
        self._initUI()

    def _initUI(self):
        """
        초기화된 화면을 보여주는 UI
        :return: None
        """
        # 위젯 설정
        tabs = QTabWidget()
        webcam_tab = WebCamTab()
        resume_tab = ResumeTab("https://kimjunheekor.github.io/about/")

        tabs.addTab(resume_tab.generateResumeTab(), self._TabInfo.tab1)
        tabs.addTab(webcam_tab.generateWebCamTab(), self._TabInfo.tab2)
        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        # 레이아웃 설정
        self.setLayout(vbox)

        # 윈도우 설정
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())