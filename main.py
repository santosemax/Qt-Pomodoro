#!/usr/local/bin/python3
import sys
from PyQt5 import QtWidgets as qtw   # Widgets/Layout Classses
from PyQt5 import QtCore as qtc      # Contains signals and slots
from PyQt5 import QtGui as qtg       # Other gui classes (fonts/colors/etc)
from PyQt5 import uic                # Import ui File

Ui_LoginForm, baseClass = uic.loadUiType('design.ui')

class MainWindow(baseClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_LoginForm()
        self.ui.setupUi(self)

        self.setFixedSize(481, 196)    


        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
