# -*- coding: utf-8 -*-

# Com_Thread
# author: Piotr Michałowski, Olsztyn, woj. W-M, Poland
# piotrm35@hotmail.com
# license: GPL v. 2
# date: 01.01.2019
# Python 3.6.7

#---------------------------------------------------------------------------------------------------------------------------------------------------------



import time
import serial
from PyQt5 import QtCore


class Com_Thread(QtCore.QThread):

    text_signal = QtCore.pyqtSignal(str)

    def __init__(self, main_frame, port, speed):
        super(Com_Thread, self).__init__(main_frame)
        self.work = False
        self.main_frame = main_frame
        self.my_com_mutex = QtCore.QMutex(QtCore.QMutex.NonRecursive)
        try:
            self.my_com = serial.Serial()
            self.my_com.port = port
            self.my_com.baudrate = speed
            self.my_com.bytesize = 8
            self.my_com.parity = 'N'
            self.my_com.stopbits = 1
            self.my_com.timeout = 1
            self.my_com.open()
            self.my_com.flushInput()
            self.my_com.flushOutput()
            self.thread_save_print("Com_Thread object is created.")
        except Exception as e:
            self.thread_save_print("Com_Thread __init__ method unexpected error: " + str(e))

            
    def run(self):
        self.thread_save_print("Com_Thread run method is started.")
        try:
            while self.work:
                if self.my_com is not None and self.my_com.isOpen():
                    self.my_com_mutex.lock()
                    _n = self.my_com.inWaiting()    # liczba bajtów oczekujących w buforze odbiorczym portu szeregowego
                    if _n > 0:
                        _txt_as_bytes = self.my_com.read(_n)
                    self.my_com_mutex.unlock()
                    if _n > 0:
                        _txt = _txt_as_bytes.decode('ascii', 'strict')
                        self.text_signal.emit(_txt)
                else:
                    self.thread_save_print("Com_Thread run method: there is no COM.")
                    break
        except Exception as e:
            self.thread_save_print("Com_Thread run method unexpected error: " + str(e))
        finally:
            if self.my_com is not None and self.my_com.isOpen():
                self.my_com.close()
                self.my_com.parent = None
            self.my_com = None
        self.work = False
        self.thread_save_print("Com_Thread run method is ended.")

        
    def Start_run(self):
        self.thread_save_print("Com_Thread run method is starting.")
        self.work = True
        self.start()
        time.sleep(0.7)

        
    def Stop_run(self):
        self.thread_save_print("Com_Thread run method is ending.")
        self.work = False
        time.sleep(0.7)
        

    def Send_text(self, text):
        try:
            if self.my_com is not None and self.my_com.isOpen():
                if len(text) > 0:
                    if self.main_frame.Show_sent_commands_checkBox.isChecked():
                        self.text_signal.emit(text + "\n")
                    self.my_com_mutex.lock()
                    self.my_com.write(text.encode('ascii', 'strict'))
                    self.my_com_mutex.unlock()
                else:
                    self.thread_save_print("Com_Thread Send_text method: there is no text to send.")
            else:
                self.thread_save_print("Com_Thread Send_text method: there is no COM.")
        except Exception as e:
            self.thread_save_print("Com_Thread Send_text method unexpected error: " + str(e))


    def thread_save_print(self, tx):
        if self.main_frame.thread_save_print_Thread is not None and self.main_frame.thread_save_print_Thread.work:
            self.main_frame.thread_save_print_Thread.print_queue.put(tx)
        else:
            print("NO thread_save_print(Com_Thread): " + tx)


        
            
            
