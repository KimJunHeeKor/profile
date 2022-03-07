from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class ResumeTab(QWidget):
    def __init__(self, homage_url):
        super(ResumeTab, self).__init__()
        # self._my_homepage_url = "https://kimjunheekor.github.io/about/"
        self._my_homepage_url = homage_url

    def generateResumeTab(self):
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