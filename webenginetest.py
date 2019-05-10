import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

web = QWebEngineView()
web.load(QUrl("https://www.wunderground.com/history/daily/KSDL/date/2018-03-29"))
web.show()

sys.exit(app.exec_())