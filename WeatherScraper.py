# Weather Scraper for Wunderground v1.0
# Written by Vu L.
# To install:
#     pip install pyqt5

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
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.htmlPath = ''
        self.threadStopped = False

        self.setWindowTitle('Wunderground Weather Scraper v1.0')
        self.setWindowIcon(QIcon('icon.png'))
        self.webEngineView = QWebEngineView()
        # self.webEngineView.setUrl(QUrl('https://www.google.com'))
        # self.webEngineView.setUrl(QUrl('https://www.wunderground.com/history/daily/KCPS/date/2017-4-2'))
        # self.webEngineView.loadFinished.connect(self.onLoadFinished)
        self.webEngineView.loadProgress.connect(self.setProgressBar)
        self.verticalLayout_2.addWidget(self.webEngineView)

        self.browseExcelFileButton.clicked.connect(self.browseCsvFile)
        self.browseSaveFolderButton.clicked.connect(self.browseSaveFolder)
        self.startButton.clicked.connect(self.getHtml)
        self.saveHtmlButton.clicked.connect(self.saveHtml)
        self.stopButton.clicked.connect(self.stopThread)
        self.goButton.clicked.connect(self.go)
        self.browseBallParkJsonButton.clicked.connect(self.browseBallParkJson)

        self.htmlTimer = QTimer()
        self.htmlTimer.timeout.connect(self.saveHtml)

        self.ballParkJsonLineEdit.setText('C:/Users/Vu/Documents/weatherscraper/ballparks.json')
        self.excelFileLineEdit.setText('C:/Users/Vu/Documents/weatherscraper/WeatherCompTable2018_vu.csv')
        self.saveFolderLineEdit.setText('C:/Users/Vu/Documents/weatherscraper/wunderground')

        ballParkJsonPath = self.ballParkJsonLineEdit.text()
        if len(ballParkJsonPath) > 0:
            self.loadBallParkJson(ballParkJsonPath)


    def go(self):
        url = self.urlLineEdit.text()
        self.webEngineView.setUrl(QUrl(url))

    def stopThread(self):
        self.statusbar.showMessage('Thread stopping...')
        self.threadStopped = True

    def setProgressBar(self, progress):
        self.progressBar.setValue(progress)

    def saveHtml(self):
        self.webEngineView.page().toHtml(self.callable)

    def loadUrl(self, msg):
        url, htmlPath = msg
        self.htmlPath = htmlPath
        self.htmlTimer.start(200)
        self.urlLineEdit.setText(url)
        self.webEngineView.setUrl(QUrl(url))
        self.statusbar.showMessage('Loading page...')

    def loadBallParkJson(self, path):
        with open(path, 'r') as f:
            self.bpdata = json.load(f)
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

    def browseCsvFile(self):
        path, fileType = QFileDialog.getOpenFileName(
            self,
            'Open Pitch CSV File',
            '',
            'CSV Files (*.csv);;All Files (*)'
        )

        self.excelFileLineEdit.setText(path)

    def browseExcelFile(self):
        path, fileType = QFileDialog.getOpenFileName(
            self,
            'Open Pitch Excel File',
            '',
            'XLSX Files (*.xlsx);;All Files (*)'
        )
        if len(path) > 0:
            self.excelFileLineEdit.setText(path)

    def browseSaveFolder(self):
        path = QFileDialog.getExistingDirectory(
            self,
            'Select the save folder',
            '',
        )
        if len(path) > 0:
            self.saveFolderLineEdit.setText(path)

    def onLoadFinished(self):
        self.statusbar.showMessage('Loading finished.')

    def callable(self, data):
        self.html = data

        if self.html.find('class="observation-table"') > 0:
            with open(self.htmlPath, 'w', encoding='utf-8') as f:
                f.write(self.html)
                self.htmlTimer.stop()
                self.statusbar.showMessage('Page source saved...OK')
                print('Page Source saved.')

    def getHtml(self):

        class getHtmlThread(QThread):
            signal = pyqtSignal('PyQt_PyObject')

            def __init__(self, main):
                QThread.__init__(self)
                self.main = main

            def run(self):
                print('Grabbing HTML files...')

                with open(self.main.excelFileLineEdit.text(), newline='') as f:
                    reader = csv.DictReader(f)

                    # rowCount = sum(1 for row in reader)
                    #
                    # print(rowCount) # 718751

                    # initialization
                    lastgameName = ''
                    gameName = ''

                    # specify a row to start from if needed
                    startRow = 0

                    for row in reader:
                        if self.main.threadStopped == True:
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
                                        CODE = self.main.bpdata[venue][each]
                                    except KeyError as error:
                                        CODE = ''
                                        print('{} was not found in ball park data'.format(str(error)))
                                        continue
                                    URL = 'https://www.wunderground.com/history/daily/{}/date/{}-{}-{}'.format(CODE,
                                                                                                               YEAR,
                                                                                                               MONTH,
                                                                                                               DAY)

                                    htmlFile = '{}_{}_{}_{}.html'.format(YEAR, MONTH, DAY, CODE)
                                    htmlFolder = self.main.saveFolderLineEdit.text()

                                    htmlPath = '/'.join((htmlFolder, htmlFile))
                                    print(URL, htmlPath)

                                    # if file exists already then skip
                                    if os.path.isfile(htmlPath):
                                        print('File already exists')
                                        continue


                                    self.signal.emit((URL, htmlPath))
                                    time.sleep(10)

                                    # while (self.main.ready == False):
                                    #     time.sleep(1)
                                lastgameName = gameName

        ballParkJson = self.ballParkJsonLineEdit.text()
        csvFile = self.excelFileLineEdit.text()
        saveFolder = self.saveFolderLineEdit.text()

        if len(ballParkJson) > 0 and len(csvFile)>0 and len(saveFolder)>0:
            self.thread = getHtmlThread(self)
            self.thread.signal.connect(self.loadUrl)
            self.thread.start()
        else:
            self.statusbar.showMessage('Please choose files/folders')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    form = App()
    form.show()
    app.exec_()

