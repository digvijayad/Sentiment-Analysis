from PyQt4 import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import random, numpy as np
import pylab as pl
import sys, time, threading
from PIL import Image
from Sentiment_analysis import Sentiment
from liveSearch_API import liveApi

class Dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        
        self.vl = QtGui.QVBoxLayout(self)
        self.display = QtGui.QTextEdit(self)
        self.vl.addWidget(self.display)
        self.display.setReadOnly(True)
        self.display.setFontPointSize(13)
        self.display.setStyleSheet("QTextEdit {background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(77, 122, 187, 248), stop:1 rgba(0, 0, 0, 255));\
                                    color: lightGrey}")

    def closeEvent(self, event):
        self.display.clear()
        print('cleared')
        self.accept()

    def aboutSoftware(self):
        self.resize(346,210)
        self.display.setLineWrapMode(0)

        self.display.setText('\tSentiment Analysis\n\
    Created By -> Digvijay Singh Naruka\n\
    Alabama State University\n\
    Version: 1.0\n\
    Build: 1000')

    def helpSoftware(self):
        self.resize(500,460)
        self.display.setText('Welcome to Sentiment Analysis App.\
This app has been developed to analyize the standings of a tennis player among his/her fans.\n\
We use the twitter API to analyize the data and show the results in the form of Pie charts, Bar and Live(real time) graphs.\n\n\
Please keep in mind that this software may take time at certain points, for example, if it does not fetch a live tweet, So kindly be patient while.\n\n\
=> To choose a tennis player from preexisting data of wimbledon 2015, click the name of the player from the drop-down list on the right hand side of the screen. \n\n\
=> You can also fetch Live tweets of Roger Federer, Novak Djokovic, Serena Williams, and Garbine Muguruza, from within thier Specific pages, by clicking the "Live Graph" radio Button\n\n\
=> To analyze live tweets, enter a player\'s name on the box available on the top left of screen. ')
 



class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.sentiment = Sentiment()
        self.sentiment.main()
##        self.live = liveApi(self.sentiment)
        self.setupUi(self)
    
    def mousePressEvent(MainWindow, event):
            if event.button() == QtCore.Qt.LeftButton:
                item = event.pos()
                but = MainWindow.lStop.frameGeometry()
                try:
                    if self.live.listen.running is True and item in but:
                        event.accept()
                    else:
                        event.ignore()
                except:
                    pass 
                print(item)
                print(but)    

    def closeEvent(MainWindow, event):
        choice= QtGui.QMessageBox.question(MainWindow,'exit','are you sure you wanna exit?',
                                   QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            try:
                if MainWindow.live:
                    MainWindow.callStop()
            except:
                pass

            print('exiting')
            event.accept()
            time.sleep(1)
        else:
            event.ignore()
            pass

    # def event(MainWindow, e):
    #     if e.type() == e.WindowStateChange:
    #         if MainWindow.windowState() & QtCore.Qt.WindowMaximized:
    #             # print(MainWindow.availableGeometry())
    #             print('changed state')
    #             MainWindow.setGeometry(10,10,667,689)
    #             return True
    #     else:
    #         e.ignore()
    #         return False

    def setupUi(self, MainWindow):
        self.setObjectName('MainWindow')
        
        # MainWindow.resize(801, 553)
        # MainWindow.setMinimumSize(871,689)
        # MainWindow.setMaximumSize(871,689)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('plastique'))
        MainWindow.setWindowTitle('Wimbledon Sentiment Analysis')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logo/wimbledon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralWidget')
        self.centralwidget.setStyleSheet('QWidget{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(77, 122, 187, 248), stop:1 rgba(0, 0, 0, 255));}'
                                         'QPushButton, QLabel,QRadioButton ,QComboBox{background-color: rgb(85, 170, 255);}'
                                         'QGroupBox,QLineEdit,{color: rgb(85, 255, 255);}'
                                         'QMenuBar {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(77, 122, 187, 248), stop:1 rgba(0, 0, 0, 255));}'
                                         'QToolBar{background-color: rgb(85, 0, 127);}')
                                         
                                         
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.stackedWidget = QtGui.QStackedWidget(self.centralwidget)
        self.startPage = QtGui.QWidget()
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.startPage)
        self.textBrowser = QtGui.QTextBrowser(self.startPage)
        self.textBrowser.setStyleSheet("border-image: url(resources/sentim.jpg); background-repeat: no-repeat; background-position:center;")
        self.verticalLayout_7.addWidget(self.textBrowser)
        self.nextButton = QtGui.QPushButton("Next", self.startPage)
        self.nextButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.nextButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.verticalLayout_7.addWidget(self.nextButton)
        self.stackedWidget.addWidget(self.startPage)
        self.mainPage = QtGui.QWidget()
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.mainPage)
        self.searchLayout = QtGui.QHBoxLayout()
        self.tweetSearch = QtGui.QLineEdit('Enter a players name to search sentiment...',self.mainPage)
##        self.tweetSearch.focusPolicy('clickFocus')
##        self.tweetSearch.setFocus(True)
        self.tweetSearch.setPlaceholderText('Enter a players name to search sentiment...')
        self.tweetSearch.setMaximumSize(QtCore.QSize(500, 16777215))
        self.tweetSearch.setToolTip("Enter a player\'s name to search sentiment about his/her live tweets")
        self.tweetSearch.setStatusTip("Search sentiment for a specific player")
        self.tweetSearch.selectAll()
        self.searchLayout.addWidget(self.tweetSearch)
        self.SearchButton = QtGui.QPushButton('Search Sentiment',self.mainPage)
        self.searchLayout.addWidget(self.SearchButton)
        self.line_2 = QtGui.QFrame(self.mainPage)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.searchLayout.addWidget(self.line_2)
        self.label = QtGui.QLabel('Choose from pre existing data:',self.mainPage)
        self.searchLayout.addWidget(self.label)
        
        
        self.playerChoice = QtGui.QComboBox(self.mainPage)
        self.playerChoice.addItem("Choose Player")
        self.playerChoice.addItem("Roger Federer")
        self.playerChoice.addItem("Novak Djokovic")
        self.playerChoice.addItem("Serena Willams")
        self.playerChoice.addItem("Garbine Muguruza")
        self.searchLayout.addWidget(self.playerChoice)
        self.verticalLayout_6.addLayout(self.searchLayout)
        self.line = QtGui.QFrame(self.mainPage)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.verticalLayout_6.addWidget(self.line)
        self.nameDisplay = QtGui.QLabel('Player Name',self.mainPage)
        self.nameDisplay.setStyleSheet('background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0.960227, y2:0.989, stop:0.488636 rgba(0, 252, 106, 248), stop:1 rgba(0, 0, 0, 255));')
        self.nameDisplay.setMaximumSize(QtCore.QSize(16777215, 35))

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(26)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.nameDisplay.setFont(font)
##        self.nameDisplay.setStyleSheet("background-color: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));")

        self.nameDisplay.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_6.addWidget(self.nameDisplay)
        self.playerStackedWidget = QtGui.QStackedWidget(self.mainPage)
        self.introPage = QtGui.QWidget()
        self.playerStackedWidget.addWidget(self.introPage)
        self.hl = QtGui.QHBoxLayout(self.introPage)
        self.imgLabel = QtGui.QLabel(self.introPage)
        self.imgLabel.setPixmap(QtGui.QPixmap('resources/touch.jpg'))
        self.hl.addWidget(self.imgLabel)
        self.dispText = QtGui.QTextEdit(self.introPage)
        self.hl.addWidget(self.dispText)
        self.dispText.setHtml('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">'
'<html><head><meta name="qrichtext" content="1" /><style type="text/css">'
'p, li { white-space: pre-wrap; }'
'</style></head><body style=" font-family:"MS Shell Dlg 2"; font-size:8pt; font-weight:400; font-style:normal;">'
'<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#55ff00;">Welcome to Sentiment Analysis App.</span></p>'
'<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#55ff00;">This app has been developed to analyize the standings of a tennis player among his/her fans.</span></p>'
'<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#55ff00;">We use the twitter API to analyize the data and show the results in the form of Pie charts, Bar and Live(real time) graphs.</span> <span style=" font-weight:600;color:#00ffff;">To choose a tennis player from preexisting data of wimbledon 2015, click the name of player from the drop-down list on the right hand side of the screen. To analyze live tweets,  enter player\'s name on the box available on the top left of screen. </span></p></body></html>')
        


        self.pageRoger = QtGui.QWidget()
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.pageRoger)
        self.rogerGraphBox = QtGui.QGroupBox('Graph Type',self.pageRoger)
        self.rogerGraphBox.setFlat(True)
        self.rogerGraphBox.setMinimumSize(QtCore.QSize(0, 50))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.rogerGraphBox)
        self.rogerPie = QtGui.QRadioButton('Pie Chart',self.rogerGraphBox)
        self.rogerPie.setChecked(False)
        self.rogerPie.setObjectName("rogerPie")
        self.horizontalLayout_5.addWidget(self.rogerPie)
        self.rogerBar = QtGui.QRadioButton('Bar Graph',self.rogerGraphBox)
        self.rogerBar.setObjectName("rogerBar")
        self.rogerBar.setChecked(True)
        self.horizontalLayout_5.addWidget(self.rogerBar)
        self.rogerLive = QtGui.QRadioButton('Live Graph',self.rogerGraphBox)
        self.rogerLive.setObjectName("rogerLive")
        self.rStop = QtGui.QPushButton('Stop Streaming', self.pageRoger)
        self.horizontalLayout_5.addWidget(self.rogerLive)
        self.verticalLayout_3.addWidget(self.rogerGraphBox)
        self.stackedWidget_2 = QtGui.QStackedWidget(self.pageRoger)
        self.piePage = QtGui.QWidget()
        self.stackedWidget_2.addWidget(self.piePage)
        self.barPage = QtGui.QWidget()
        self.stackedWidget_2.addWidget(self.barPage)
        self.rlivePage = QtGui.QWidget()
        self.stackedWidget_2.addWidget(self.rlivePage)
        self.verticalLayout_3.addWidget(self.stackedWidget_2)
        self.verticalLayout_3.addWidget(self.rStop)
        self.playerStackedWidget.addWidget(self.pageRoger)

        self.pageNovak = QtGui.QWidget()
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.pageNovak)
        self.novakGraphBox = QtGui.QGroupBox('Graph Type',self.pageNovak)
        self.novakGraphBox.setMinimumSize(QtCore.QSize(0, 50))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.novakGraphBox)
        self.novakPie = QtGui.QRadioButton('Pie Chart',self.novakGraphBox)
        self.novakPie.setChecked(False)
        self.novakPie.setObjectName("novakPie")
        self.horizontalLayout_6.addWidget(self.novakPie)
        self.novakBar = QtGui.QRadioButton('Bar Graph',self.novakGraphBox)
        self.novakBar.setObjectName("novakBar")
        self.novakBar.setChecked(True)
        self.horizontalLayout_6.addWidget(self.novakBar)
        self.novakLive = QtGui.QRadioButton('Live Graph',self.novakGraphBox)
        self.novakLive.setObjectName("novakLive")
        self.nStop = QtGui.QPushButton('Stop Streaming', self.pageNovak)
        self.horizontalLayout_6.addWidget(self.novakLive)
        self.verticalLayout_4.addWidget(self.novakGraphBox)
        self.stackedWidget_3 = QtGui.QStackedWidget(self.pageNovak)
        self.novakPiePage = QtGui.QWidget()
        self.stackedWidget_3.addWidget(self.novakPiePage)
        self.novakBarPage = QtGui.QWidget()
        self.stackedWidget_3.addWidget(self.novakBarPage)
        self.novakLivePage = QtGui.QWidget()
        self.stackedWidget_3.addWidget(self.novakLivePage)
        self.verticalLayout_4.addWidget(self.stackedWidget_3)
        self.verticalLayout_4.addWidget(self.nStop)
        self.playerStackedWidget.addWidget(self.pageNovak)

        self.pageSerena = QtGui.QWidget()
        self.verticalLayout = QtGui.QVBoxLayout(self.pageSerena)
        self.serenaGraphBox = QtGui.QGroupBox('Graph Type',self.pageSerena)
        self.serenaGraphBox.setMinimumSize(QtCore.QSize(0, 50))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.serenaGraphBox)
        self.serenaPie = QtGui.QRadioButton('Pie Chart',self.serenaGraphBox)
        self.serenaPie.setChecked(False)
        self.serenaPie.setObjectName("serenaPie")
        self.horizontalLayout_4.addWidget(self.serenaPie)
        self.serenaBar = QtGui.QRadioButton('Bar Graph',self.serenaGraphBox)
        self.serenaBar.setObjectName("serenaBar")
        self.serenaBar.setChecked(True)
        self.horizontalLayout_4.addWidget(self.serenaBar)
        self.serenaLive = QtGui.QRadioButton('Live Graph',self.serenaGraphBox)
        self.serenaLive.setObjectName("serenaLive")
        self.horizontalLayout_4.addWidget(self.serenaLive)
        self.verticalLayout.addWidget(self.serenaGraphBox)
        self.stackedWidget_4 = QtGui.QStackedWidget(self.pageSerena)
        self.serPiePage = QtGui.QWidget()
        self.stackedWidget_4.addWidget(self.serPiePage)
        self.serBarPage = QtGui.QWidget()
        self.stackedWidget_4.addWidget(self.serBarPage)
        self.serLivePage = QtGui.QWidget()
        self.stackedWidget_4.addWidget(self.serLivePage)
        self.verticalLayout.addWidget(self.stackedWidget_4)
        self.sStop = QtGui.QPushButton('Stop Streaming', self.pageSerena)
        self.verticalLayout.addWidget(self.sStop)
        self.playerStackedWidget.addWidget(self.pageSerena)

        self.pageGarbi = QtGui.QWidget()
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.pageGarbi)
        self.GarbiGraphBox = QtGui.QGroupBox('Graph Type',self.pageGarbi)
        self.GarbiGraphBox.setMinimumSize(QtCore.QSize(0, 50))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.GarbiGraphBox)
        self.garbiPie = QtGui.QRadioButton('Pie Chart',self.GarbiGraphBox)
        self.garbiPie.setChecked(False)
        self.garbiPie.setObjectName("garbiPie")
        self.horizontalLayout_7.addWidget(self.garbiPie)
        self.garbiBar = QtGui.QRadioButton('Bar Graph',self.GarbiGraphBox)
        self.garbiBar.setObjectName("garbiBar")
        self.garbiBar.setChecked(True)
        self.horizontalLayout_7.addWidget(self.garbiBar)
        self.garbiLive = QtGui.QRadioButton('Live Graph',self.GarbiGraphBox)
        self.garbiLive.setObjectName("garbiLive")
        self.horizontalLayout_7.addWidget(self.garbiLive)
        self.verticalLayout_5.addWidget(self.GarbiGraphBox)
        self.stackedWidget_5 = QtGui.QStackedWidget(self.pageGarbi)
        self.garPiePage = QtGui.QWidget()
        self.stackedWidget_5.addWidget(self.garPiePage)
        self.garBarPage = QtGui.QWidget()
        self.stackedWidget_5.addWidget(self.garBarPage)
        self.garLivePage = QtGui.QWidget()
        self.GarbiGraphBox.raise_()
        self.stackedWidget_5.addWidget(self.garLivePage)
        self.verticalLayout_5.addWidget(self.stackedWidget_5)
        self.gStop = QtGui.QPushButton('Stop Streaming', self.pageGarbi)
        self.verticalLayout_5.addWidget(self.gStop)
        self.playerStackedWidget.addWidget(self.pageGarbi)

        self.pageLive = QtGui.QWidget()
        self.lStop = QtGui.QPushButton('Stop Streaming', self.pageLive)
        self.lStop.setMaximumSize(100,20)
        self.lStop.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.vl = QtGui.QVBoxLayout(self.pageLive)
        self.vl.setDirection(3) #Bottom To Top
        self.vl.addWidget(self.lStop)

        self.playerStackedWidget.addWidget(self.pageLive)


        self.verticalLayout_6.addWidget(self.playerStackedWidget)
        self.stackedWidget.addWidget(self.mainPage)
        self.verticalLayout_2.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        #Menu Bar
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(77, 122, 187, 248), stop:1 rgba(0, 0, 0, 255));')
        self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 21))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuHelp = QtGui.QMenu(self.menubar)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.setStyleSheet('background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0.960227, y2:0.989, stop:0.488636 rgba(0, 252, 106, 248), stop:1 rgba(0, 0, 0, 255));')
        self.toolBar = QtGui.QToolBar(MainWindow)
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar.setStyleSheet('background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0.960227, y2:0.989, stop:0.488636 rgba(0, 252, 106, 248), stop:1 rgba(0, 0, 0, 255));')
        self.toolBar.setMovable(False)

        self.actionExit = QtGui.QAction('&Exit',MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.setShortcut("Ctrl+Q")

        self.actionHelp = QtGui.QAction('About',MainWindow)
        self.actionVersion = QtGui.QAction('Version', MainWindow)
        
        self.menuFile.setTitle("File")
        self.menuHelp.setTitle( "Help")
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionVersion)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.actionExit.setStatusTip('Exit the file')
        self.actionExit.setWhatsThis('Closes the program')
        self.actionExit.setToolTip('Click to exit this program!')        
        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)
        self.playerStackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
        self.stackedWidget_3.setCurrentIndex(0)
        self.stackedWidget_4.setCurrentIndex(0)
        self.stackedWidget_5.setCurrentIndex(0)
       

    def retranslateUi(self):
        self.playerChoice.setStatusTip("Analyize pre-existing data")
        self.SearchButton.setStatusTip("Search about a particular player")
        self.player = self.playerChoice.currentText()
        self.lStop.setStatusTip("Stop Streaming")
        self.rStop.setStatusTip("Stop Streaming")
        self.nStop.setStatusTip("Stop Streaming")
        self.sStop.setStatusTip("Stop Streaming")
        self.gStop.setStatusTip("Stop Streaming")
        self.lStop.setToolTip("Click the Button to stop streaming the current live graph")
        self.rStop.setToolTip("Click the Button to stop streaming the current live graph")
        self.nStop.setToolTip("Click the Button to stop streaming the current live graph")
        self.sStop.setToolTip("Click the Button to stop streaming the current live graph")
        self.gStop.setToolTip("Click the Button to stop streaming the current live graph")
        self.radioGroup()
        self.connect()


    def connect(self):

        QtCore.QObject.connect(self.SearchButton, QtCore.SIGNAL('clicked()'), self.callLive)
        # self.SearchButton.clicked.connect(lambda: self.playerStackedWidget.setCurrentIndex(5))
        # QtCore.QObject.connect(self.tweetSearch, QtCore.SIGNAL('textEdited(QString)'), self.nameDisplay.setText)
        # self.SearchButton.clicked.connect(lambda: self.nameDisplay.setText(self.tweetSearch.text()))
        # self.SearchButton.clicked.connect(lambda: self.connectLive(self.tweetSearch.text()))
        self.actionExit.triggered.connect(self.close)
        self.actionHelp.triggered.connect(self.helpDialog)
        self.actionVersion.triggered.connect(self.versionDialog)
        self.rBox.buttonClicked.connect(self.connectGraphType)
        self.nBox.buttonClicked.connect(self.connectGraphType)
        self.sBox.buttonClicked.connect(self.connectGraphType)
        self.gBox.buttonClicked.connect(self.connectGraphType)
        self.nextButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.nextButton.clicked.connect(self.nameDisplay.hide)
        QtCore.QObject.connect(self.playerChoice, QtCore.SIGNAL("currentIndexChanged(int)"), self.playerStackedWidget.setCurrentIndex)
        QtCore.QObject.connect(self.playerChoice, QtCore.SIGNAL("activated(QString)"), self.nameDisplay.setText)
        QtCore.QObject.connect(self.playerChoice, QtCore.SIGNAL("currentIndexChanged(int)"), (self.connectGraphType))
        QtCore.QObject.connect(self.playerChoice, QtCore.SIGNAL("currentIndexChanged(int)"), (self.hideName))
        QtCore.QMetaObject.connectSlotsByName(self)
        QtCore.QObject.connect(self.tweetSearch, QtCore.SIGNAL('textEdited(QString)'), self.disableButton)
        QtCore.QObject.connect(self.lStop, QtCore.SIGNAL('clicked()'), self.callStop)
        QtCore.QObject.connect(self.sStop, QtCore.SIGNAL('clicked()'), self.callStop)
        QtCore.QObject.connect(self.rStop, QtCore.SIGNAL('clicked()'), self.callStop)
        QtCore.QObject.connect(self.nStop, QtCore.SIGNAL('clicked()'), self.callStop)
        QtCore.QObject.connect(self.gStop, QtCore.SIGNAL('clicked()'), self.callStop)


    
    def versionDialog(self):
        dialog = Dialog()
        dialog.aboutSoftware()
        dialog.exec()

    def helpDialog(self):
        dialog = Dialog()
        dialog.helpSoftware()
        dialog.exec()        

    def callStop(self):

        try:
            # if self.live.listen.running == True:
            self.live.stopStream()
        except BaseException as e:
            pass
            print(e)

    def callLive(self):        
        # if self.vl.count() > 1:
        #     self.vl.itemAt(1).widget().close()
        # for i in range(self.vl.count()):
        #     print (i)
        #     print(self.vl.itemAt(i).widget())
        self.nameDisplay.show()
        self.lStop.show()
        self.playerStackedWidget.setCurrentIndex(5)
        self.nameDisplay.setText(self.tweetSearch.text())
        self.liveGraph()
        choice = QtGui.QMessageBox.question(self, "Live Graph",
                        "This option may take sometime depending on your internet and computer speed!\n Are you sure you want to continue?",
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print ("Live Graph")
            try:
                name = self.tweetSearch.text()
                t2 = threading.Thread(target =self.connectLive, args=(name,))
                t2.start()
            except:
                raise
        

    def liveGraph(self):
        
        style.use('ggplot')        
        self.livefigure = plt.figure(facecolor='#1f5990')
        self.livecanvas = FigureCanvas(self.livefigure)
        page  =self.pageLive
        if not self.vl.count() > 1:
            self.vl.addWidget(self.livecanvas)
       
        ax1 = self.livefigure.add_subplot(111)

        def animate(i):
            graph_data = open('data/bar','r').read()
            lines = graph_data.split('\n')
            length = len(lines)-1
            # print(length)
            xs = ["total","pos","neg","neut"]
            ys = [0,0,0,0]
            if length > 1:
                i,j,l,m = lines[length-1].split(',')
                ys[0]+=int(i)
                ys[1]+=int(j)
                ys[2]+=int(l)
                ys[3]+=int(m)

            width = 0.5
            name = self.nameDisplay.text()
            plt.subplots_adjust(left=0.06, right=1.0, bottom=0.09, top=0.963)
            ax1.clear()

            bars = ax1.bar(range(len(xs)), ys, width=width, alpha=0.7, label= name, color = 'kgrb')
            ax1.set_ylabel('NO OF TWEETS')

            ax1.set_xticks(np.arange(len(xs)) + width/2)
            ax1.set_xticklabels(xs, rotation=0)
            ax1.xaxis.label.set_color('white')
            ax1.yaxis.label.set_color('white')
            ax1.tick_params(axis='x', colors='white')
            ax1.tick_params(axis='y', colors='white')
            
            top = ys[0]+10
            im = Image.open('resources/tennisL.jpg' ).rotate(0)
            ax1.imshow(im, origin='upper',alpha=1,extent=[0,4,0,top],aspect='auto')
            ax1.legend()

            try:
                if self.live.getTimeOut() is True:
                    QtGui.QMessageBox.warning(self, "Time Out Error", "No Tweets Fetched!!")
                    self.callStop()
                    self.live.listen.timeOut=None
            except:
                pass

        ani = animation.FuncAnimation(self.livefigure, animate, interval=2000)
        

        self.livecanvas.draw()


    def connectLive(self, text):
        self.lStop.show()
        self.live = liveApi(self.sentiment)
        self.callStop() #Stop the streaming if it is already running
        self.live.runStream(text)


    def disableButton(self):
        if 'Enter ' in self.tweetSearch.text() or self.tweetSearch.text()== '':
            self.SearchButton.setEnabled(False)
        else:
            self.SearchButton.setEnabled(True)
            
    def hideName(self):
        if self.playerStackedWidget.currentIndex() == 0:
            self.nameDisplay.hide()
        else:
            self.nameDisplay.show()
            if 'Enter ' in self.tweetSearch.text() or self.tweetSearch.text()== '':
                self.SearchButton.setEnabled(False)
            else:
                self.SearchButton.setEnabled(True)
        
    def radioGroup(self):
        #ADD RADIO BUTTON GROPUS
        self.rBox = QtGui.QButtonGroup(self.rogerGraphBox)
        self.rBox.setObjectName('rBox')
        self.rBox.addButton(self.rogerPie,1)
        self.rBox.addButton(self.rogerBar,2)
        self.rBox.addButton(self.rogerLive,3)
        self.nBox = QtGui.QButtonGroup(self.novakGraphBox)
        self.nBox.setObjectName('nBox')
        self.nBox.addButton(self.novakPie,1)
        self.nBox.addButton(self.novakBar,2)
        self.nBox.addButton(self.novakLive,3)
        self.sBox = QtGui.QButtonGroup(self.serenaGraphBox)
        self.sBox.setObjectName('sBox')
        self.sBox.addButton(self.serenaPie,1)
        self.sBox.addButton(self.serenaBar,2)
        self.sBox.addButton(self.serenaLive,3)
        self.gBox = QtGui.QButtonGroup(self.GarbiGraphBox)
        self.gBox.setObjectName('gBox')
        self.gBox.addButton(self.garbiPie,1)
        self.gBox.addButton(self.garbiBar,2)
        self.gBox.addButton(self.garbiLive,3)

    def rPGraph(self):
        self.piefigure = plt.figure(1,figsize=(5,5))#1, figsize=(3,3), facecolor='white')
        self.piecanvas = FigureCanvas(self.piefigure)
        self.piefigure.add_subplot(111)
        layout = QtGui.QVBoxLayout(self.piePage)
    
        layout.addWidget(self.piecanvas)
        '''plotting pie'''
        #random
        ax =plt.axes([0.1,0.1,0.8,0.8])

        labels='Positive', 'Negative', 'Neutral'
        ax.hold(True)
        fracs = (self.rpos, self.rneg, self.rneut)
        colors = ['green','red','blue']

        im = Image.open('resources/fed.jpg' ).rotate(180)
        plt.imshow(im, origin='lower', extent=[0,1,0,1],aspect='auto')

        plt.pie(fracs, labels= labels, colors=colors, autopct='%1.1f%%', shadow=True)
        plt.title('Roger Federer', bbox={'facecolor':'0.8', 'pad':5})

        plt.gca().set_aspect('1')
##        plt.show()

        
    def rLGraph(self):
        #Pie
        style.use('ggplot')        
        self.rlivefigure = plt.figure(facecolor='#1f5990')
        self.rlivecanvas = FigureCanvas(self.rlivefigure)
        
        layout = QtGui.QVBoxLayout(self.rlivePage)
        layout.addWidget(self.rlivecanvas)
        # layout.addWidget(self.rStop)
        ax1 = self.rlivefigure.add_subplot(111)

        def animate(i):
            graph_data = open('data/bar','r').read()
            lines = graph_data.split('\n')
            length = len(lines)-1
            # print(length)
            xs = ["total","pos","neg","neut"]
            ys = [0,0,0,0]
            if length > 1:
                i,j,l,m = lines[length-1].split(',')
                ys[0]+=int(i)
                ys[1]+=int(j)
                ys[2]+=int(l)
                ys[3]+=int(m)

            width = 0.5
            plt.subplots_adjust(left=0.06, right=1.0, bottom=0.09, top=0.963)
            ax1.clear()
            ax1.bar(range(len(xs)), ys, width=width, alpha=0.5, label = 'Roger Federer', color = 'orange')
            ax1.set_ylabel('NO OF TWEETS')
            ax1.set_xticks(np.arange(len(xs)) + width/2)
            ax1.set_xticklabels(xs, rotation=0)
            ax1.xaxis.label.set_color('white')
            ax1.yaxis.label.set_color('white')
            ax1.tick_params(axis='x', colors='white')
            ax1.tick_params(axis='y', colors='white')
            
            top = ys[0]+10
            im = Image.open('resources/rogerL.jpg' ).rotate(0)
            ax1.imshow(im, origin='upper',alpha=1,extent=[0,4,0,top],aspect='auto')
            ax1.legend()

        ani = animation.FuncAnimation(self.rlivefigure, animate, interval=2000)

        self.rlivecanvas.draw()
        
        
    def rBGraph(self):
        #BAR

        self.rbarfigure = plt.figure(facecolor='#550505')
        self.rbarcanvas = FigureCanvas(self.rbarfigure)

        layout1 = QtGui.QVBoxLayout(self.barPage)
##        self.rbartoolbar = NavigationToolbar(self.rbarcanvas, self.barPage)
##        layout1.addWidget(self.rbartoolbar)
        layout1.addWidget(self.rbarcanvas)

        print('button pressed')
        
        number = []
        tweet = []

        for line in self.rdata.split("\n"):
            x, y = line.split()
            number.append(int(x))
            tweet.append(y)
        
        ax =self.rbarfigure.add_subplot(111)
        ax.hold(False)
        plt.subplots_adjust(left=0.09, right=1.0, bottom=0.09, top=0.963)
        
        width=0.5
        ax.hold(True)
        ax.bar(range(len(tweet)), number, width=width,alpha=0.5,label='Roger Federer', color='red')
        ax.set_xticks(np.arange(len(tweet)) + width/2)
        ax.set_xticklabels(tweet, rotation=0)
        ax.set_ylabel('NO OF TWEETS')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        im = Image.open('resources/roger.jpg' ).rotate(0)
        ax.imshow(im, origin='upper',alpha=1,extent=[0,4,0,self.rtotal+1000],aspect='auto')
        ax.legend()
##        self.rbarfigure.show()
        
        self.rbarcanvas.draw()

        

    def nPGraph(self):
        #Pie
        self.npiefigure = plt.figure(1, figsize=(3,3), facecolor='white')
        self.npiecanvas = FigureCanvas(self.npiefigure)
        self.npiefigure.add_subplot(111)
        layout = QtGui.QVBoxLayout(self.novakPiePage)
    
        layout.addWidget(self.npiecanvas)
        '''plotting pie'''
        #random
        ax =plt.axes([0.1,0.1,0.8,0.8])

        labels='Positive', 'Negative', 'Neutral'
        colors = ['green','red','blue']
        fracs = (self.npos, self.nneg, self.nneut)
        plt.pie(fracs, labels= labels,colors=colors, autopct='%1.1f%%', shadow=True) 
        plt.title('Novak Djokovic', bbox={'facecolor':'0.8', 'pad':5})

        plt.gca().set_aspect('1')

        
        
    def nBGraph(self):
        #BAR
        self.nbarfigure = plt.figure(facecolor='#03220c')
        self.nbarcanvas = FigureCanvas(self.nbarfigure)

        layout1 = QtGui.QVBoxLayout(self.novakBarPage)
##        self.nbartoolbar = NavigationToolbar(self.nbarcanvas, self.novakBarPage)
##        layout1.addWidget(self.nbartoolbar)
        layout1.addWidget(self.nbarcanvas)

        print('button pressed')
        
        number = []
        tweet = []

        for line in self.ndata.split("\n"):
            x, y = line.split()
            number.append(int(x))
            tweet.append(y)
        
        
        ax =self.nbarfigure.add_subplot(111)
        plt.subplots_adjust(left=0.09, right=1.0, bottom=0.06, top=0.963)
        ax.hold(True)
        width=0.5
        ax.bar(range(len(tweet)), number, width=width,label="Novak Djokovic", color='#ff5a00',alpha=0.5)
        ax.set_xticks(np.arange(len(tweet)) + width/2)
        ax.set_xticklabels(tweet, rotation=0)
        ax.set_ylabel('NO OF TWEETS')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        im = Image.open('resources/novak2.jpg' ).rotate(0)
        ax.imshow(im, origin='upper',alpha=1,extent=[0,4,0,self.ntotal+1000],aspect='auto')
        ax.legend()
        self.nbarcanvas.draw()

    def nLGraph(self):
        #live
        self.nlivefigure = plt.figure(facecolor = 'white')
        self.nlivecanvas = FigureCanvas(self.nlivefigure)

        layout = QtGui.QVBoxLayout(self.novakLivePage)
        layout.addWidget(self.nlivecanvas)
        ax1 = self.nlivefigure.add_subplot(111)
        def animate(i):
            graph_data = open('data/bar','r').read()
            lines = graph_data.split('\n')
            length = len(lines)-1
            # print(length)
            xs = ["total","pos","neg","neut"]
            ys = [0,0,0,0]
            if length > 1:
                i,j,l,m = lines[length-1].split(',')
                ys[0]+=int(i)
                ys[1]+=int(j)
                ys[2]+=int(l)
                ys[3]+=int(m)

            width = 0.5
            plt.subplots_adjust(left=0.06, right=1.0, bottom=0.09, top=0.963)
            ax1.clear()
            ax1.bar(range(len(xs)), ys, width=width, alpha=0.5, label = 'Novak Djokovic', color = 'red')
            ax1.set_ylabel('NO OF TWEETS')
            ax1.set_xticks(np.arange(len(xs)) + width/2)
            ax1.set_xticklabels(xs, rotation=0)
            ax1.xaxis.label.set_color('w')
            ax1.yaxis.label.set_color('black')
            ax1.tick_params(axis='x', colors='k')
            ax1.tick_params(axis='y', colors='k')
            
            top = ys[0]+10
            im = Image.open('resources/novak.jpg' ).rotate(0)
            ax1.imshow(im, origin='upper',alpha=1,extent=[0,4,0,top],aspect='auto')
            ax1.legend()

        
        ani = animation.FuncAnimation(self.nlivefigure, animate, interval=2000)
        self.nlivecanvas.draw()
        

    def sPGraph(self):
        #Pie
        self.piefigure = plt.figure(1, figsize=(3,3), facecolor='white')
        self.piecanvas = FigureCanvas(self.piefigure)
        self.piefigure.add_subplot(111)
        layout = QtGui.QVBoxLayout(self.serPiePage)
    
        layout.addWidget(self.piecanvas)
        '''plotting pie'''
        #random
        ax =plt.axes([0.1,0.1,0.8,0.8])
        colors = ['green','red','blue']
        labels='Positive', 'Negative', 'Neutral'

        fracs = (self.spos, self.sneg, self.sneut)
        plt.pie(fracs, labels= labels,colors=colors, autopct='%1.1f%%', shadow=True) 
        plt.title('Serena Willams', bbox={'facecolor':'0.8', 'pad':5})

        plt.gca().set_aspect('1')

        
        
    def sBGraph(self):
        #BAR
        self.barfigure = plt.figure(facecolor='#2d2f2e')
        self.barcanvas = FigureCanvas(self.barfigure)

        layout1 = QtGui.QVBoxLayout(self.serBarPage)
##        self.bartoolbar = NavigationToolbar(self.barcanvas, self.barPage)
##        layout1.addWidget(self.bartoolbar)
        layout1.addWidget(self.barcanvas)

        print('button pressed')
        
        number = []
        tweet = []

        for line in self.sdata.split("\n"):
            x, y = line.split()
            number.append(int(x))
            tweet.append(y)
        
##        ax =self.barfigure.add_subplot(111)
        ax =plt.subplot()
        plt.subplots_adjust(left=0.09, right=1.0, bottom=0.06, top=0.963)
        ax.hold(True)
        width=0.5
        ax.bar(range(len(tweet)), number, width=width,label="Serena Willams", color='white', alpha =0.5)
        ax.set_xticks(np.arange(len(tweet)) + width/2,)
        ax.set_xticklabels(tweet, rotation=0)
        ax.set_ylabel('NO OF TWEETS')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        im = Image.open('resources/serena.jpg' ).rotate(0)
        ax.imshow(im, origin='upper',alpha=1,extent=[0,4,0,self.stotal+100],aspect='auto')
        ax.legend()
        self.barcanvas.draw()

    def sLGraph(self):
        #Pie
        self.slivefigure = plt.figure(facecolor = '#2d2f2e')
        self.slivecanvas = FigureCanvas(self.slivefigure)

        layout = QtGui.QVBoxLayout(self.serLivePage)

        layout.addWidget(self.slivecanvas)
        ax1 = self.slivefigure.add_subplot(111)

        def animate(i):
            graph_data = open('data/bar','r').read()
            lines = graph_data.split('\n')
            length = len(lines)-1
            # print(length)
            xs = ["total","pos","neg","neut"]
            ys = [0,0,0,0]
            if length > 1:
                i,j,l,m = lines[length-1].split(',')
                ys[0]+=int(i)
                ys[1]+=int(j)
                ys[2]+=int(l)
                ys[3]+=int(m)

            width = 0.5
            plt.subplots_adjust(left=0.06, right=1.0, bottom=0.09, top=0.963)
            ax1.clear()
            ax1.bar(range(len(xs)), ys, width=width, alpha=0.5, label = 'Serena Willams', color = 'white')
            ax1.set_ylabel('NO OF TWEETS')
            ax1.set_xticks(np.arange(len(xs)) + width/2)
            ax1.set_xticklabels(xs, rotation=0)
            ax1.xaxis.label.set_color('white')
            ax1.yaxis.label.set_color('white')
            ax1.tick_params(axis='x', colors='white')
            ax1.tick_params(axis='y', colors='white')
            
            top = ys[0]+10
            im = Image.open('resources/serena1.jpg' ).rotate(0)
            ax1.imshow(im, origin='upper',alpha=1,extent=[0,4,0,top],aspect='auto')
            ax1.legend()

        
        ani = animation.FuncAnimation(self.slivefigure, animate, interval=2000)
        self.slivecanvas.draw()


    def gPGraph(self):
        #Pie
        self.piefigure = plt.figure(1, figsize=(3,3), facecolor='white')
        self.piecanvas = FigureCanvas(self.piefigure)
        self.piefigure.add_subplot(111)
        layout = QtGui.QVBoxLayout(self.garPiePage)
    
        layout.addWidget(self.piecanvas)
        '''plotting pie'''
        #random
        ax =plt.axes([0.1,0.1,0.8,0.8])
        colors = ['green','red','blue']
        labels='Positive', 'Negative', 'Neutral'

        fracs = (self.gpos, self.gneg, self.gneut)
        plt.pie(fracs, labels= labels, colors=colors,autopct='%1.1f%%', shadow=True) 
        plt.title('Garbine Muguruza', bbox={'facecolor':'0.8', 'pad':5})

        plt.gca().set_aspect('1')

        
        
    def gBGraph(self):
        #BAR
        self.barfigure = plt.figure(facecolor='#1f5990')
        self.barcanvas = FigureCanvas(self.barfigure)

        layout1 = QtGui.QVBoxLayout(self.garBarPage)
##        self.bartoolbar = NavigationToolbar(self.barcanvas, self.barPage)
##        layout1.addWidget(self.bartoolbar)
        layout1.addWidget(self.barcanvas)

        print('button pressed')
        
        number = []
        tweet = []

        for line in self.gdata.split("\n"):
            x, y = line.split()
            number.append(int(x))
            tweet.append(y)

        ax =plt.subplot()
        plt.subplots_adjust(left=0.09, right=1.0, bottom=0.06, top=0.963)
        ax.hold(True)
        width=0.5
        ax.bar(range(len(tweet)), number, width=width,label="Garbine Muguruza", color='#db6626', alpha=0.5)
        ax.set_xticks(np.arange(len(tweet)) + width/2)
        ax.set_xticklabels(tweet, rotation=0)
        ax.set_ylabel('NO OF TWEETS')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        im = Image.open('resources/garbine.jpg' ).rotate(0)
        ax.imshow(im, origin='upper',alpha=1,extent=[0,4,0,self.gtotal+100],aspect='auto')
        ax.legend()
        self.barcanvas.draw()

    def gLGraph(self):
        #Pie
        self.glivefigure = plt.figure(facecolor='#1f5990')
        self.glivecanvas = FigureCanvas(self.glivefigure)

        layout = QtGui.QVBoxLayout(self.garLivePage)
        layout.addWidget(self.glivecanvas)
        ax1 = self.glivefigure.add_subplot(111)

        def animate(i):
            graph_data = open('data/bar','r').read()
            lines = graph_data.split('\n')
            length = len(lines)-1
            # print(length)
            xs = ["total","pos","neg","neut"]
            ys = [0,0,0,0]
            if length > 1:
                i,j,l,m = lines[length-1].split(',')
                ys[0]+=int(i)
                ys[1]+=int(j)
                ys[2]+=int(l)
                ys[3]+=int(m)

            width = 0.5
            plt.subplots_adjust(left=0.06, right=1.0, bottom=0.09, top=0.963)
            ax1.clear()
            ax1.bar(range(len(xs)), ys, width=width, alpha=0.5, label = 'Garbine Muguruza', color='#db6626')
            ax1.set_ylabel('NO OF TWEETS')
            ax1.set_xticks(np.arange(len(xs)) + width/2)
            ax1.set_xticklabels(xs, rotation=0)
            ax1.xaxis.label.set_color('white')
            ax1.yaxis.label.set_color('white')
            ax1.tick_params(axis='x', colors='white')
            ax1.tick_params(axis='y', colors='white')
            
            top = ys[0]+10
            im = Image.open('resources/garbine1.jpg' ).rotate(0)
            ax1.imshow(im, origin='upper',alpha=1,extent=[0,4,0,top],aspect='auto')
            ax1.legend()

        
        ani = animation.FuncAnimation(self.glivefigure, animate, interval=2000)
        self.glivecanvas.draw()

    def connectGraphType(self,):
        plt.close()
        player = self.playerChoice.currentText()
        print(player)
##        self.sender = self.MainWindow.sender().objectName()
##        print(self.sender)
##        print(self.rBox.checkedButton().text())
##        print(self.rBox.checkedButton().objectName())
##        print(self.rBox.checkedId())
        if 'Roger' in player:
            print('roger')

            self.rdata = self.sentiment.rdata
            self.rpos = self.sentiment.rpos
            self.rneg = self.sentiment.rneg
            self.rneut = self.sentiment.rneut
            self.rtotal = self.sentiment.rtotal
            
            if self.rBox.checkedButton().objectName() == 'rogerBar':
                self.stackedWidget_2.setCurrentIndex(1)
                self.rStop.hide()
                self.rBGraph()

            if self.rBox.checkedButton().objectName() == 'rogerPie':
                self.stackedWidget_2.setCurrentIndex(0)
                self.rStop.hide()
                self.rPGraph()
                
                
            if self.rBox.checkedButton().objectName() == 'rogerLive':
                self.stackedWidget_2.setCurrentIndex(2)
                self.rStop.show()
                self.rStop.setMaximumSize(100,20000)
                self.rStop.setLayoutDirection(QtCore.Qt.RightToLeft)
                self.rLGraph()
                choice = QtGui.QMessageBox.question(self, "Live Graph",
                                "This option may take sometime depending on your internet and computer speed!\n Are you sure you want to continue?",
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                if choice == QtGui.QMessageBox.Yes:
                    print ("Live Graph")
                    try:
                        t2 = threading.Thread(target =self.connectLive, args=('\"@rogerfederer\", "#Federer\"', ))
                        t2.start()
                    except:
                        raise

                
        elif 'Novak' in player:
            print('novak')
            self.ndata = self.sentiment.ndata
            self.npos = self.sentiment.npos
            self.nneg = self.sentiment.nneg
            self.nneut = self.sentiment.nneut
            self.ntotal = self.sentiment.ntotal
            
            if self.nBox.checkedButton().objectName() == 'novakBar':
                self.stackedWidget_3.setCurrentIndex(1)
                self.nStop.hide()
                self.nBGraph()
                
            if self.nBox.checkedButton().objectName() == 'novakPie':
                self.stackedWidget_3.setCurrentIndex(0)
                self.nStop.hide()
                self.nPGraph()
                
            if self.nBox.checkedButton().objectName() == 'novakLive':
                self.stackedWidget_3.setCurrentIndex(2)
                self.nStop.show()
                self.nStop.setMaximumSize(100,20)
                self.nStop.setLayoutDirection(QtCore.Qt.RightToLeft)
                self.nLGraph()
                choice = QtGui.QMessageBox.question(self, "Live Graph",
                        "This option may take sometime depending on your internet and computer speed!\n Are you sure you want to continue?",
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                if choice == QtGui.QMessageBox.Yes:
                    print ("Live Graph")
                    try:
                        t2 = threading.Thread(target =self.connectLive, args=('\"@DjokerNole\",\"#NoleFam\"',))
                        t2.start()
                    except:
                        raise

        elif 'Serena' in player:
            self.sdata = self.sentiment.ndata
            self.spos = self.sentiment.spos
            self.sneg = self.sentiment.sneg
            self.sneut = self.sentiment.sneut
            self.stotal = self.sentiment.stotal
            
            if self.sBox.checkedButton().objectName() == 'serenaBar':
                self.stackedWidget_4.setCurrentIndex(1)
                self.sStop.hide()
                self.sBGraph()
            if self.sBox.checkedButton().objectName() == 'serenaPie':
                self.stackedWidget_4.setCurrentIndex(0)
                self.sStop.hide()
                self.sPGraph()

            if self.sBox.checkedButton().objectName() == 'serenaLive':
                self.stackedWidget_4.setCurrentIndex(2)
                self.sStop.show()
                self.sStop.setMaximumSize(100,20)
                self.sStop.setLayoutDirection(QtCore.Qt.RightToLeft)
                self.sLGraph()
                choice = QtGui.QMessageBox.question(self, "Live Graph",
                        "This option may take sometime depending on your internet and computer speed!\n Are you sure you want to continue?",
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                if choice == QtGui.QMessageBox.Yes:
                    print ("Live Graph")
                    try:
                        t2 = threading.Thread(target =self.connectLive, args=('\"serenawilliams\", \"serena\", \"williams\"',))
                        t2.start()
                    except:
                        raise
                
        elif 'Garbi' in player:
            self.gdata = self.sentiment.gdata
            self.gpos = self.sentiment.gpos
            self.gneg = self.sentiment.gneg
            self.gneut = self.sentiment.gneut
            self.gtotal = self.sentiment.gtotal
            
            if self.gBox.checkedButton().objectName() == 'garbiBar':
                self.stackedWidget_5.setCurrentIndex(1)
                self.gStop.hide()
                self.gBGraph()
            if self.gBox.checkedButton().objectName() == 'garbiPie':
                self.stackedWidget_5.setCurrentIndex(0)
                self.gStop.hide()
                self.gPGraph()
            if self.gBox.checkedButton().objectName() == 'garbiLive':
                self.stackedWidget_5.setCurrentIndex(2)
                self.gStop.show()
                self.gStop.setMaximumSize(100,20)
                self.gStop.setLayoutDirection(QtCore.Qt.RightToLeft)
                self.gLGraph()
                
                choice = QtGui.QMessageBox.question(self, "Live Graph",
                        "This option may take sometime depending on your internet and computer speed!\n Are you sure you want to continue?",
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                if choice == QtGui.QMessageBox.Yes:
                    print ("Live Graph")
                    try:
                        t2 = threading.Thread(target =self.connectLive, args=('@GarbiMuguruza',))
                        t2.start()
                    except:
                        raise

        
import Logos_rc
import images_rc

if __name__ == "__main__":
    import sys, time
    app = QtGui.QApplication(sys.argv)

    # Create and display the splash screen
    splash_pix = QtGui.QPixmap('resources/sentiment_splash.gif')
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
   
    Ui=Ui_MainWindow()
    Ui.show()

    splash.finish(Ui)
    sys.exit(app.exec_())
