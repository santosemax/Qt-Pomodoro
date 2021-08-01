#!/usr/local/bin/python3
import sys, time 
from PyQt5 import QtWidgets as qtw   # Widgets/Layout Classses
from PyQt5 import QtCore as qtc      # Contains signals and slots from PyQt5 import QtGui as qtg       
from PyQt5 import uic                # (Fonts/colors/etc) (Unused)
from design import Ui_Form
from editTime import Ui_Form as editWin

# Handles all timer functions
class Thread(qtc.QThread):
    time_signal = qtc.pyqtSignal(list)

    active = False
    isStarted = False
    break_active = False
    rotationTime = 25
    breakTime = 5
    longTime = 15
    Min, Sec = rotationTime, 0
    progress = 0

    def run(self):
        while self.Min >= 0 and self.isStarted: 
            self.active = True
            self.Sec -= 1
            if self.Sec == -1:
                self.Min -= 1
                self.Sec = 59
                # Break Logic
                if self.Min < 0:
                    self.break_active = not self.break_active
                    if self.break_active == True:
                        self.Min = self.breakTime
                        self.Sec = 0
                        self.isStarted = False
                        print("-- Break Time Started --")
                    else:
                        self.Min = self.rotationTime
                        self.Sec = 0
                        self.isStarted = False
                        print("-- Break Time Ended --")
            self.time_signal.emit([self.Min, self.Sec])
            if self.break_active != True:
                self.progress += 1
            time.sleep(1.0)

# Edit Timer Window
class editWindow(qtw.QWidget):
    time_variables =  qtc.pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = editWin()
        self.ui.setupUi(self) 
        self.setFixedSize(372, 105)
        self.setWindowTitle("Configure Timer")
        self.setWindowFlags(qtc.Qt.WindowStaysOnTopHint | qtc.Qt.FramelessWindowHint)

        self.ui.cancel_button.clicked.connect(self.exit)
        self.ui.apply_button.clicked.connect(self.apply)
    

    def apply(self):
        self.time_variables.emit([
            self.ui.rotation_time.currentText()[0:2],
            self.ui.break_time.currentText()[0:2],
            self.ui.long_break_time.currentText()[0:2]
        ])
        # print(f"{int(self.ui.long_break_time.currentText()[0:2])}") # Debug Line
        self.close()

    def exit(self):
        self.close()


class MainWindow(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Code Starts Here
        self.ui = Ui_Form()
        self.ui.setupUi(self) 
        self.setFixedSize(481, 196)
        self.setWindowTitle("QT Pomo - Timer")
        self.thread = Thread()
        self.w = editWindow()
        self.active = False

        self.ui.start_button.clicked.connect(self.start_timer)
        self.ui.pause_button.clicked.connect(self.stop_timer)
        self.ui.reset_button.clicked.connect(self.reset_timer)
        self.ui.edit_button.clicked.connect(self.edit_timer)
        self.ui.pause_button.setEnabled(False)
        self.ui.progressBar.setMaximum((self.thread.Min * 60) * 3)
        
        # Code ends here
        self.show()

    # Timer signal (using class above)
    def start_timer(self):
        if self.thread.active == False: 
            self.thread.time_signal.connect(self.function_thread)
        self.thread.start()
        self.thread.isStarted = True
        #self.ui.start_button.setEnabled(False)
        self.ui.pause_button.setEnabled(True)

    # Stop signal to pause the timer
    def stop_timer(self):
        self.thread.isStarted = False
        self.ui.start_button.setEnabled(True)
        self.ui.pause_button.setEnabled(False)
        if self.thread.isStarted == True:
            self.ui.start_button.setText("Resume")

    def reset_timer(self):
        self.thread.Min = 25
        self.thread.Sec = 0
        self.ui.timer.setText(f"{self.thread.Min}:{self.thread.Sec:02}")
        self.ui.start_button.setEnabled(True)
        self.ui.pause_button.setEnabled(False)
        self.ui.start_button.setText("Start")

    def edit_timer(self):
        self.w.show()
        # Connecting Signals to Slot
        self.w.time_variables.connect(self.edit_function)

    # Timer Slot
    def function_thread(self, signal): 
        self.ui.timer.setText(f"{signal[0]}:{signal[1]:02}")
        self.ui.progressBar.setValue(self.thread.progress)
        print(signal) # Debug Line

    # Edit Time Slot
    def edit_function(self, variables):
        self.thread.Min = int(variables[0])
        self.thread.rotationTime = int(variables[0])
        self.thread.breakTime = int(variables[1])
        self.thread.longTime = int(variables[2])
        self.thread.Sec = 0
        print(f"Rotation Time: {variables[0]}, Break Time: {variables[1]}, Long Time:  {variables[2]}") # Debug Line
        self.ui.timer.setText(f"{int(variables[0])}:00")
        self.thread.isStarted = False
        self.ui.start_button.setEnabled(True)
        self.ui.pause_button.setEnabled(False)
        self.ui.start_button.setText("Start")



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow()    
    sys.exit(app.exec_())
