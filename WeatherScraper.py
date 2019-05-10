# Weather Scraper for Wunderground v1.0
# Written by Vu L.

# Install these dependencies:
# pip install pyqt5==5.12.2
# pip install pyqtwebengine==5.12.1

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

        # window size settings and restore
        self.settings = QSettings('WeatherScraper', 'WeatherScraper')
        width = self.settings.value('windowWidth', type=int)
        height = self.settings.value('windowHeight', type=int)
        self.resize(width, height)

        self.htmlPath = ''

        # thread for reading pitch file
        self.thread = None

        self.setWindowTitle('Wunderground Weather Scraper v1.0')
        self.setWindowIcon(QIcon(':/icon/icon.png'))
        self.webEngineView = QWebEngineView()

        self.verticalLayout_2.addWidget(self.webEngineView)

        # button connections
        self.browseCsvFileButton.clicked.connect(self.browseCsvFile)
        self.browseSaveFolderButton.clicked.connect(self.browseSaveFolder)
        self.startButton.clicked.connect(self.getHtml)
        self.saveHtmlButton.clicked.connect(self.saveHtml)
        self.stopButton.clicked.connect(self.stopThread)
        self.goButton.clicked.connect(self.go)
        self.browseBallParkJsonButton.clicked.connect(self.browseBallParkJson)

        # timer to check if html has what we need
        self.htmlTimer = QTimer()
        self.htmlTimer.timeout.connect(self.saveHtml)

        # restore last saved settings
        self.ballParkJsonLineEdit.setText(self.settings.value('ballParkJsonPath', type=str))
        self.csvFileLineEdit.setText(self.settings.value('csvFilePath', type=str))
        self.saveFolderLineEdit.setText(self.settings.value('saveFolder', type=str))

    def resizeEvent(self, *args, **kwargs):
        self.settings.setValue('windowWidth', self.width())
        self.settings.setValue('windowHeight', self.height())

    def go(self):
        """Load the web url shown in url line edit."""
        url = self.urlLineEdit.text()
        adjustedUrl = QUrl.fromUserInput(url)
        self.webEngineView.load(adjustedUrl)
        self.urlLineEdit.setText(adjustedUrl.toString())

    def stopThread(self):
        """Stop the html grabbing thread."""
        self.statusbar.showMessage('Thread stopping...')
        print('Thread stopping...')
        self.thread.stop()

    def setProgressBar(self, progress):
        """Set the progress of the progress bar."""
        self.progressBar.setValue(progress)

    def setStatusBarMessage(self, msg):
        """Set the message of the status bar."""
        self.statusbar.showMessage(msg)

    def saveHtml(self):
        """Save the html file to disk."""
        path, fileType = QFileDialog.getSaveFileName(
            self,
            'Save HTML File',
            '',
            'HTML Files (*.html);;All Files (*)'
        )
        if len(path) > 0:
            self.htmlPath = path
            self.webEngineView.page().toHtml(self.callable)

    def loadUrl(self, msg):
        """Call function within thread to load url."""
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

        self.webEngineView.load(QUrl(url))
        self.setProgressBar(progress)
        self.statusbar.showMessage('Loading page...')

    def loadBallParkJson(self, path):
        """Load ball park data in JSON format."""
        with open(path, 'r') as f:
            self.bpData = json.load(f)
            self.statusbar.showMessage('Ball park JSON loaded...')

    def browseBallParkJson(self):
        """Open file dialog and select ball park JSON file."""
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
        """Open file dialog and select csv file."""
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
        """Open folder dialog and select folder to save html files."""
        path = QFileDialog.getExistingDirectory(
            self,
            'Select the save folder',
            '',
        )
        if len(path) > 0:
            self.saveFolderLineEdit.setText(path)
            self.settings.setValue('saveFolder', path)

    def callable(self, data):
        """Call function for asynchronous html loading."""
        self.html = data

        if self.html.find('class="observation-table"') > 0:
            with open(self.htmlPath, 'w', encoding='utf-8') as f:
                f.write(self.html)
                self.htmlTimer.stop()
                self.statusbar.showMessage('Loading finished. Page source saved.')
                print('Loading finished. Page source saved.')

    def getHtml(self):
        """Thread to get all html files for pitch file."""
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

