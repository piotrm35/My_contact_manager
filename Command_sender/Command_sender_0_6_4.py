# -*- coding: utf-8 -*-

SCRIPT_TITLE = 'Command sender'
SCRIPT_NAME = 'Command_sender'
SCRIPT_VERSION = '0.6.4'
GENERAL_INFO = u"""
author: Piotr Michałowski, Olsztyn, woj. W-M, Poland
piotrm35@hotmail.com
license: GPL v. 2
work begin: 01.01.2019
"""

# Python 3.6.7

import os, sys, time, datetime
from PyQt5 import QtCore, QtGui, QtWidgets, uic
try:
    from Com_Thread_0_6_1 import Com_Thread
    from MyLineEdit import MyLineEdit
    from Thread_save_print_Thread_0_3_0 import Thread_save_print_Thread
except:
    from Command_sender.Com_Thread_0_6_1 import Com_Thread
    from Command_sender.MyLineEdit import MyLineEdit
    from Command_sender.Thread_save_print_Thread_0_3_0 import Thread_save_print_Thread
    

#====================================================================================================================


class Command_sender(QtWidgets.QWidget):
    def __init__(self, parent = None, initial_port = None):
        super(Command_sender, self).__init__()
        self.parent = parent
        self.base_path = os.path.realpath(__file__).split(os.sep + SCRIPT_NAME + os.sep)[0] + os.sep + SCRIPT_NAME
        uic.loadUi(os.path.join(self.base_path, 'ui', 'Command_sender.ui'), self)
        self.setWindowTitle(SCRIPT_TITLE + ' v. ' + SCRIPT_VERSION)
        self.thread_save_print_Thread = None
        self.com_thread = None
        self.main_textEdit_mutex = QtCore.QMutex(QtCore.QMutex.NonRecursive)
        self.Speed_comboBox.setCurrentIndex(12)             # (i - 1) zmieniono, bo USB_switch ma 9600 b/s
        self.Command_lineEdit = MyLineEdit(self.centralwidget)
        self.Command_lineEdit.setGeometry(QtCore.QRect(10, 530, 389, 20))
        self.Command_lineEdit.setObjectName("Command_lineEdit")
        # obsługa przycisków i in.:
        self.Start_pushButton.clicked.connect(self.Start_handleButton)
        self.Stop_pushButton.clicked.connect(self.Stop_handleButton)
        self.Send_command_pushButton.clicked.connect(self.Send_command_handleButton)
        self.Clear_main_textEdit_pushButton.clicked.connect(self.Clear_main_textEdit_handleButton)
        self.About_pushButton.clicked.connect(self.About_handleButton)
        self.Send_CTRL_X_pushButton.clicked.connect(self.Send_CTRL_X_handleButton)
        self.Send_CTRL_Z_pushButton.clicked.connect(self.Send_CTRL_Z_handleButton)
        self.Stop_pushButton.setEnabled(False)
        self.Send_command_pushButton.setEnabled(False)
        self.Send_CTRL_X_pushButton.setEnabled(False)
        self.Send_CTRL_Z_pushButton.setEnabled(False)
        self.Command_lineEdit.enter_pressed_signal.connect(self.Send_command_handleButton)
        if initial_port is not None:
            index = self.Port_comboBox.findText(initial_port, QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.Port_comboBox.setCurrentIndex(index)
                self.Start_handleButton()


    def __del__(self):
        self.on_close()
		
    def closeEvent(self, event):        # overriding the method
        if self.parent is not None:
            self.parent.Command_sender_is_hiding()
        #event.accept()


    def on_close(self):
        try:
            self.Start_pushButton.clicked.disconnect(self.Start_handleButton)
            self.Stop_pushButton.clicked.disconnect(self.Stop_handleButton)
            self.Send_command_pushButton.clicked.disconnect(self.Send_command_handleButton)
            self.Clear_main_textEdit_pushButton.clicked.disconnect(self.Clear_main_textEdit_handleButton)
            self.About_pushButton.clicked.disconnect(self.About_handleButton)
            self.Send_CTRL_X_pushButton.clicked.disconnect(self.Send_CTRL_X_handleButton)
            self.Send_CTRL_Z_pushButton.clicked.disconnect(self.Send_CTRL_Z_handleButton)
            self.Command_lineEdit.enter_pressed_signal.disconnect(self.Send_command_handleButton)
        except:
            pass
        self.All_Thread_close()
        

    #----------------------------------------------------------------------------------------------------------------
    # input widget methods


    @QtCore.pyqtSlot(str)
    def Main_textEdit_set_text(self, tx):
        self.main_textEdit_mutex.lock()
        if tx is not None and len(tx) > 0:
            _time_str = '[' + str(datetime.datetime.now().strftime('%H:%M')) + '] -> '
            self.Main_textEdit.insertPlainText(_time_str + tx)
            self.Main_textEdit.verticalScrollBar().setValue(self.Main_textEdit.verticalScrollBar().maximum())
        else:
            self.thread_save_print("Main_textEdit_set_text method: There is nothing to write.")
        self.main_textEdit_mutex.unlock()


    def Clear_main_textEdit_handleButton(self):
        self.main_textEdit_mutex.lock()
        self.Main_textEdit.clear()
        self.main_textEdit_mutex.unlock()

        
    def Start_handleButton(self):
        try:
            self.thread_save_print_Thread = Thread_save_print_Thread(self)
            self.thread_save_print_Thread.Start_run()
            time.sleep(0.5)
            self.com_thread = Com_Thread(self, str(self.Port_comboBox.currentText()), self.Speed_comboBox.currentText())
            self.com_thread.Start_run()
            self.com_thread.text_signal.connect(self.Main_textEdit_set_text)
            self.Port_comboBox.setEnabled(False)
            self.Speed_comboBox.setEnabled(False)
            self.Start_pushButton.setEnabled(False)
            self.Stop_pushButton.setEnabled(True)
            self.Send_command_pushButton.setEnabled(True)
            self.Send_CTRL_X_pushButton.setEnabled(True)
            self.Send_CTRL_Z_pushButton.setEnabled(True)
        except Exception as e:
            self.thread_save_print("Start_handleButton method unexpected error: " + str(e))


    def All_Thread_close(self):
        try:
            if self.com_thread is not None and self.com_thread.work:
                self.com_thread.text_signal.disconnect(self.Main_textEdit_set_text)
                self.com_thread.Stop_run()
                self.com_thread.parent = None
        except Exception as e:
            self.thread_save_print("All_Thread_close method unexpected error(1): " + str(e))
        finally:
            self.com_thread = None
        try:
            if self.thread_save_print_Thread is not None and self.thread_save_print_Thread.work:
                self.thread_save_print_Thread.Stop_run()
                self.thread_save_print_Thread.parent = None
        except Exception as e:
            self.thread_save_print("All_Thread_close method unexpected error(2): " + str(e))
        finally:
            self.thread_save_print_Thread = None


    def Stop_handleButton(self):
        self.Port_comboBox.setEnabled(True)
        self.Speed_comboBox.setEnabled(True)
        self.Start_pushButton.setEnabled(True)
        self.Stop_pushButton.setEnabled(False)
        self.Send_command_pushButton.setEnabled(False)
        self.Send_CTRL_X_pushButton.setEnabled(False)
        self.Send_CTRL_Z_pushButton.setEnabled(False)
        self.All_Thread_close()


    def About_handleButton(self):
        QtWidgets.QMessageBox.information(self, SCRIPT_TITLE, SCRIPT_TITLE + ' v. ' + SCRIPT_VERSION + '\n' + GENERAL_INFO)


    def Send_command_handleButton(self):
        if self.com_thread is not None:
            _text = str(self.Command_lineEdit.text())
            if self.CR_at_the_end_checkBox.isChecked():
                _text += "\r"                                       # wymagane dla komend AT
            self.com_thread.Send_text(_text)
            time.sleep(0.5)
        else:
            self.thread_save_print("Send_command_handleButton method: self.com_thread is None.")

    def Send_command(self, command):
        if self.com_thread is not None:
            self.Command_lineEdit.setText(command)
            self.Send_command_handleButton()
        else:
            self.thread_save_print("Send_command method: self.com_thread is None.")


    def Send_CTRL_X_handleButton(self):
        if self.com_thread is not None:
            _text = chr(0x18)                                       # CTRL+X przerwanie wysyłania komendy AT
            self.com_thread.Send_text(_text)
            time.sleep(0.5)
        else:
            self.thread_save_print("Send_CTRL_X_handleButton method: self.com_thread is None.")


    def Send_CTRL_Z_handleButton(self):
        if self.com_thread is not None:
            _text = chr(0x1A)                                       # CTRL+Z wymagane dla SMS (koniec linii tekstowej)
            self.com_thread.Send_text(_text)
            time.sleep(0.5)
        else:
            self.thread_save_print("Send_CTRL_Z_handleButton method: self.com_thread is None.")


    def thread_save_print(self, tx):
        if self.thread_save_print_Thread is not None and self.thread_save_print_Thread.work:
            self.thread_save_print_Thread.print_queue.put(tx)
        else:
            print("NO thread_save_print: " + tx)
        

#====================================================================================================================

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    command_sender = Command_sender()
    command_sender.show()
    sys.exit(app.exec_())


