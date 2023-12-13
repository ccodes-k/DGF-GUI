from PyQt5 import QtWidgets
import sys
from GUI.GUI_Base_Structure import Ui_MainWindow

if __name__ == "__main__":
    ''' To Run the whole code
        input: None
        Output: None ''' 
    
    app = QtWidgets.QApplication(sys.argv)
    Monitor = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Monitor)
    Monitor.showMaximized()
    sys.exit(app.exec_())
