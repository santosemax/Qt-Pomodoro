#!/usr/local/bin/python3
import sys, time, pdb
from PyQt5 import QtWidgets as qtw   # Widgets/Layout Classses
from PyQt5 import QtCore as qtc      # Contains signals and slots
from PyQt5 import QtGui as qtg       # Other gui classes (fonts/colors/etc)
from PyQt5 import uic                # Import ui File
from design import Ui_Form

class Signals(qtc.QObject):
    time_signal = qtc.pyqtSignal(list)

class Thread(qtc.QRunnable):
    signal = qtc.pyqtSignal(int)

    def __init__(self):
        super(Thread, self).__init__()
        self.signal = Signals()

    @qtc.pyqtSlot()
    def run(self):
        Min, Sec = 24, 60
        while Min != 0:
            Sec -= 1
            time.sleep(1.0)
            if Sec == -1:
                Min -= 1
                Sec = 59
            self.signal.time_signal.emit([Min, Sec])



class MainWindow(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Code Starts Here
        self.ui = Ui_Form()
        self.ui.setupUi(self) # setupUi builds the GUI we designed onto the QWidget
        self.setFixedSize(481, 196)
        self.setWindowTitle("QT Pomo - Timer")
        self.threadpool = qtc.QThreadPool()

        # Button Functions
        #self.ui.start_button.clicked.connect(self.thread)
        self.ui.start_button.clicked.connect(self.click_start)

        # Code ends here
        self.show()

    # Timer Signal (using class above)
    def click_start(self):
        thread = Thread()
        thread.signal.time_signal.connect(self.function_thread)
        self.threadpool.start(thread)

    # Timer Slot
    def function_thread(self, signal):
        self.ui.timer.setText(f"{signal[0]}:{signal[1]:02}")
        print(signal)

    # Thread Here:
     




    # Thread for Timer Start
    # def thread(self):
    #     t1 = Thread(target=self.start_timer)
    #     t1.start()


    # Slot for Starting the Timer (Needs to be Threaded or will freeze)
    #def start_timer(self):
    #    Min, Sec = 24, 60
    #    while Min != 0:
    #        Sec -= 1
    #        time.sleep(1.0)
    #        if Sec == -1:
    #            Min -= 1
    #            Sec = 59
    #        self.ui.timer.setText(f"{Min}:{Sec:02}")


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
