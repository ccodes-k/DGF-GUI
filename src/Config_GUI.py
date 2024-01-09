#UI for config window

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from utils.server import Runner

class ConfigWindow(QWidget):
    OpenFile = 0
    OpenFiles = 1
    OpenDirectory = 2
    SaveFile = 3

    def __init__(self, mode=OpenFile):
        '''
            Setting up the window
        '''
        super(ConfigWindow, self).__init__()
        self.p = None

        # window setup
        self.resize(1000, 700)
        self.setWindowTitle("Data Viewer")
        self.browser_mode = mode
        self.filter_name = 'All files (*.*)'
        self.dirpath = QtCore.QDir.currentPath()

        # Placeholder for the server variable
        self.server = None



        self.initUI()

    def initUI(self):
        '''
            Displaying window elements and assigning their functions
        '''
        # text
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setFixedWidth(180)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.move(5, 10)

        # buttons
        self.pb1 = QtWidgets.QPushButton(self)
        self.pb1.setText("Send data")
        self.pb1.move(390, 600)
        self.pb1.clicked.connect(self.start)
        
        self.pb2 = QtWidgets.QPushButton(self)
        self.pb2.setText("Stop")
        self.pb2.move(500, 600)
        self.pb2.clicked.connect(self.process_finished)

        self.pb3 = QtWidgets.QPushButton(self)
        self.pb3.setText("OK")
        self.pb3.move(445, 640)
        self.pb3.clicked.connect(lambda:self.close())

        self.pb4 = QtWidgets.QPushButton(self)
        self.pb4.setText("Search")
        self.pb4.move(200, 8)
        self.pb4.clicked.connect(self.getFile)

        self.pb5 = QtWidgets.QPushButton(self)
        self.pb5.setText("Calibrate")
        self.pb5.move(300, 8)
        self.pb5.clicked.connect(self.openFileNameDialog)

        # checkboxes
        self.b1 = QtWidgets.QCheckBox("Camera feed",self)
        self.b1.move(275, 560)
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
        
        self.b2 = QtWidgets.QCheckBox("Temp",self)
        self.b2.move(385, 560)
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))

        self.b3 = QtWidgets.QCheckBox("IMU",self)
        self.b3.move(455, 560)
        self.b3.toggled.connect(lambda:self.btnstate(self.b3))

        self.b4 = QtWidgets.QCheckBox("GPS",self)
        self.b4.move(515, 560)
        self.b4.toggled.connect(lambda:self.btnstate(self.b4))

        self.b5 = QtWidgets.QCheckBox("Sonar",self)
        self.b5.move(575, 560)
        self.b5.toggled.connect(lambda:self.btnstate(self.b5))

        self.b6 = QtWidgets.QCheckBox("Heart Rate",self)
        self.b6.move(645, 560)
        self.b6.toggled.connect(lambda:self.btnstate(self.b6))

        # text box
        self.textbox = QtWidgets.QPlainTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.move(140,50)
        self.textbox.resize(700,500)

        def setFileFilter(text):
            self.filter_name = text

        def setDefaultDir(path):
            self.dirpath = path
        
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

    '''
        Directory for choosing calibration file
    '''
    # browse file to choose the calibration for camera
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            with open(fileName, 'r') as file:
                print(file.read())
    
    def getFile(self):
        self.filepaths = []
        
        if self.browser_mode == ConfigWindow.OpenFile:
            self.filepaths.append(QFileDialog.getOpenFileName(self, caption='Choose File',
                                                    directory=self.dirpath,
                                                    filter=self.filter_name)[0])
        elif self.browser_mode == ConfigWindow.OpenFiles:
            self.filepaths.extend(QFileDialog.getOpenFileNames(self, caption='Choose Files',
                                                    directory=self.dirpath,
                                                    filter=self.filter_name)[0])
        elif self.browser_mode == ConfigWindow.OpenDirectory:
            self.filepaths.append(QFileDialog.getExistingDirectory(self, caption='Choose Directory',
                                                    directory=self.dirpath))
        else:
            options = QFileDialog.Options()
            if sys.platform == 'darwin':
                options |= QFileDialog.DontUseNativeDialog
            self.filepaths.append(QFileDialog.getSaveFileName(self, caption='Save/Save As',
                                                    directory=self.dirpath,
                                                    filter=self.filter_name,
                                                    options=options)[0])
        if len(self.filepaths) == 0:
            return
        elif len(self.filepaths) == 1:
            self.lineEdit.setText(self.filepaths[0])
        else:
            self.lineEdit.setText(",".join(self.filepaths))
        
    def openFile(self):
        open(self.filepaths).read()

    def getPaths(self):
        return self.filepaths
    
    '''
        Selected arguments starts specific threads in another program
    '''
    # run selected checkbox
    def start_functions(self):
        self.functions = ""
        if self.b1.isChecked():
            self.functions+= ' -im'
        if self.b2.isChecked():
            self.functions+= ' -t'
        if self.b3.isChecked():
            self.functions+= ' -i'
        if self.b4.isChecked():
            self.functions+= ' -g'
        if self.b5.isChecked():
            self.functions+= ' -s'
        if self.b6.isChecked():
            self.functions+= ' -hr'        
        # print(self.functions)
        return self.functions
    
    

    # check state of checkbox
    def btnstate(self,b):

        if b.text() == "Camera feed":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")

        if b.text() == "Temp":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")
				
        if b.text() == "IMU":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")
        
        if b.text() == "GPS":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")

        if b.text() == "Sonar":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")
        
        if b.text() == "Heart Rate":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")


    # display text in textbox
    def message(self, s):
        self.textbox.appendPlainText(s)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    # display state of process
    def handle_state(self, state):
        states = {
            QtCore.QProcess.NotRunning: 'Not running',
            QtCore.QProcess.Starting: 'Starting',
            QtCore.QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    # start python program to communicate
    def start(self):
        '''
            Start communication program
        '''
        if self.p is None:
            self.message("Executing process")
            self.p = QtCore.QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.stateChanged.connect(self.handle_state)
            # self.p.start("python3", self.start_functions())
            print(r"python3 ./utils/server1.py" + self.start_functions())
            # self.p.start(r"python3 .\utils\server.py" + self.start_functions())
            self.server, self.threads = Runner(image = self.b1.isChecked(),
                                               temperature = self.b2.isChecked(),
                                               IMU=self.b3.isChecked(),
                                               GPS=self.b4.isChecked(),
                                               sonar=self.b5.isChecked(),
                                               heartrate=self.b6.isChecked())

            # print("start")

    # stop python program
    def process_finished(self):
        '''
            Stop program
        '''
        self.message("Process finished.")
        self.p = None


def data_viewer():
    app = QApplication(sys.argv)
    win = ConfigWindow()
    win.show()
    sys.exit(app.exec_())

# start the UI
#data_viewer()