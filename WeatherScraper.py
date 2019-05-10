# Weather Scraper for Wunderground v1.0
# Written by Vu L.
#
# Install these dependences:
# pip install pyqt5
# pip install PyQtWebEngine

import sys
import os
import csv
import json
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from WeatherScraperUI import Ui_MainWindow

class App(QMainWindow, Ui_MainWindow):
    # resized = pyqtSignal()
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.settings = QSettings('WeatherScraper', 'WeatherScraper')
        width = self.settings.value('windowWidth', type=int)
        height = self.settings.value('windowHeight', type=int)
        self.resize(width, height)

        self.htmlPath = ''
        self.thread = None

        self.setWindowTitle('Wunderground Weather Scraper v1.0')
        self.setWindowIcon(QIcon('icon.png'))
        self.webEngineView = QWebEngineView()

        self.verticalLayout_2.addWidget(self.webEngineView)

        self.browseCsvFileButton.clicked.connect(self.browseCsvFile)
        self.browseSaveFolderButton.clicked.connect(self.browseSaveFolder)
        self.startButton.clicked.connect(self.getHtml)
        self.saveHtmlButton.clicked.connect(self.saveHtml)
        self.stopButton.clicked.connect(self.stopThread)

        self.goButton.clicked.connect(self.go)
        self.browseBallParkJsonButton.clicked.connect(self.browseBallParkJson)

        self.htmlTimer = QTimer()
        self.htmlTimer.timeout.connect(self.saveHtml)

        self.ballParkJsonLineEdit.setText(self.settings.value('ballParkJsonPath', type=str))
        self.csvFileLineEdit.setText(self.settings.value('csvFilePath', type=str))
        self.saveFolderLineEdit.setText(self.settings.value('saveFolder', type=str))


    def resizeEvent(self, *args, **kwargs):
        self.settings.setValue('windowWidth', self.width())
        self.settings.setValue('windowHeight', self.height())
        # self.resized.emit()

    def go(self):
        url = self.urlLineEdit.text()
        self.webEngineView.setUrl(QUrl(url))

    def stopThread(self):
        self.statusbar.showMessage('Thread stopping...')
        print('Thread stopping...')
        self.thread.stop()

    def setProgressBar(self, progress):
        self.progressBar.setValue(progress)

    def setStatusBarMessage(self, msg):
        self.statusbar.showMessage(msg)

    def saveHtml(self):
        self.webEngineView.page().toHtml(self.callable)
        # pass

    def loadUrl(self, msg):
        url, htmlPath, progress = msg

        self.htmlPath = htmlPath
        self.htmlTimer.start(200)
        self.urlLineEdit.setText(url)
        self.webEngineView.page().profile().clearAllVisitedLinks()
        self.webEngineView.page().profile().setCachePath(self.saveFolderLineEdit.text())
        self.webEngineView.page().profile().clearHttpCache()
        # self.webEngineView.page().profile().AllowPersistentCookies = False
        # self.webEngineView.page().profile().setHttpCacheType(0)
        self.webEngineView.page().profile().setHttpUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36')
        # self.webEngineView.setUrl(QUrl(url)
        self.webEngineView.load(QUrl(url))
        self.setProgressBar(progress)
        self.statusbar.showMessage('Loading page...')

    def loadBallParkJson(self, path):
        with open(path, 'r') as f:
            self.bpData = json.load(f)
            self.statusbar.showMessage('Ball park JSON loaded...')

    def browseBallParkJson(self):
        path, fileType = QFileDialog.getOpenFileName(
            self,
            'Open Ball Park JSON Data',
            '',
            'JSON Files (*.json);;All Files (*)'
        )
        if len(path) > 0:
            self.ballParkJsonLineEdit.setText(path)
            self.loadBallParkJson(path)
            self.settings.setValue('ballParkJsonPath', path)

    def browseCsvFile(self):
        path, fileType = QFileDialog.getOpenFileName(
            self,
            'Open Pitch CSV File',
            '',
            'CSV Files (*.csv);;All Files (*)'
        )
        if len(path) > 0:
            self.csvFileLineEdit.setText(path)
            self.settings.setValue('csvFilePath', path)


    def browseSaveFolder(self):
        path = QFileDialog.getExistingDirectory(
            self,
            'Select the save folder',
            '',
        )
        if len(path) > 0:
            self.saveFolderLineEdit.setText(path)
            self.settings.setValue('saveFolder', path)

    def onLoadFinished(self):
        self.statusbar.showMessage('Loading finished.')

    def callable(self, data):
        self.html = data

        if self.html.find('class="observation-table"') > 0:
            with open(self.htmlPath, 'w', encoding='utf-8') as f:
                f.write(self.html)
                self.htmlTimer.stop()
                self.statusbar.showMessage('Loading finished. Page source saved.')
                print('Loading finished. Page source saved.')

    def getHtml(self):
        class getHtmlThread(QThread):
            signal = pyqtSignal('PyQt_PyObject')
            message = pyqtSignal('PyQt_PyObject')

            def __init__(self):
                QThread.__init__(self)
                self.delay = None
                self.bpData = None
                self.csvFile = None
                self.saveFolder = None
                self.stopped = False

            def stop(self):
                self.stopped = True

            def run(self):
                self.message.emit('Grabbing HTML files...')
                print('Grabbing HTML files...')

                with open(self.csvFile, newline='') as f:
                    reader = csv.DictReader(f)

                    lineCount = sum(1 for row in reader)

                    # print(lineCount) # 718751

                    # initialization
                    lastgameName = ''
                    gameName = ''

                    # specify a row to start from if needed
                    startRow = 0

                    # go back to beginning to read from the top
                    f.seek(0)
                    reader = csv.DictReader(f)

                    for row in reader:
                        if self.stopped:
                            break

                        ap_list = ['closest_ap1_code', 'closest_ap2_code', 'closest_ap3_code']

                        if (reader.line_num >= startRow):
                            gameName = row['gameName']
                            venue = row['venue']
                            gameNameSplit = gameName.split(sep='_')

                            YEAR = gameNameSplit[1]
                            MONTH = gameNameSplit[2]
                            DAY = gameNameSplit[3]

                            # if gameName is different than the last one, then pull html
                            if gameName != lastgameName:
                                # print(YEAR, MONTH, DAY)
                                for each in ap_list:
                                    try:
                                        CODE = self.bpData[venue][each]
                                    except KeyError as error:
                                        CODE = ''
                                        print('{} was not found in ball park data'.format(str(error)))
                                        continue
                                    URL = 'https://www.wunderground.com/history/daily/{}/date/{}-{}-{}'.format(CODE,
                                                                                                               YEAR,
                                                                                                               MONTH,
                                                                                                               DAY)

                                    htmlFile = '{}_{}_{}_{}.html'.format(YEAR, MONTH, DAY, CODE)
                                    htmlFolder = self.saveFolder

                                    htmlPath = '/'.join((htmlFolder, htmlFile))
                                    print(URL, htmlPath)

                                    # if file exists already then skip
                                    if os.path.isfile(htmlPath):
                                        print('File already exists')
                                        continue

                                    progress = int(round(reader.line_num / lineCount * 100))
                                    # print(progress)

                                    self.signal.emit((URL, htmlPath, progress))
                                    time.sleep(self.delay)

                                lastgameName = gameName

        ballParkJson = self.ballParkJsonLineEdit.text()
        csvFile = self.csvFileLineEdit.text()
        saveFolder = self.saveFolderLineEdit.text()

        if len(ballParkJson) > 0 and len(csvFile) > 0 and len(saveFolder) > 0:
            self.loadBallParkJson(self.ballParkJsonLineEdit.text())
            self.thread = getHtmlThread()
            self.thread.csvFile = self.csvFileLineEdit.text()
            self.thread.bpData = self.bpData
            self.thread.saveFolder = self.saveFolderLineEdit.text()
            self.thread.delay = self.timerSpinBox.value()
            self.thread.signal.connect(self.loadUrl)
            self.thread.message.connect(self.setStatusBarMessage)
            self.thread.start()
        else:
            self.statusbar.showMessage('Please choose files/folders')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    form = App()
    form.show()
    app.exec_()

