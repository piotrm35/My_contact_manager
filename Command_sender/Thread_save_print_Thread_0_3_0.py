# -*- coding: utf-8 -*-

# Thread_save_print_Thread
# author: Piotr Michałowski, Olsztyn, woj. W-M, Poland
# piotrm35@hotmail.com
# license: GPL v. 2
# date: 07.04.2019
# Python 3.6.7

#---------------------------------------------------------------------------------------------------------------------------------------------------------


# only this thread can use print function


import time
from PyQt5 import QtCore
from queue import Queue, Empty


class Thread_save_print_Thread(QtCore.QThread):

    def __init__(self, main_frame):
        super(Thread_save_print_Thread, self).__init__(main_frame)
        self.work = False
        self.print_queue = Queue()
        print("Thread_save_print_Thread object is created.")

            
    def run(self):
        print("Thread_save_print_Thread run method is started.")
        while self.work:
            while not self.print_queue.empty():
                try:
                    print(self.print_queue.get(block = False))
                except Empty:
                    break
                except Exception as e:
                    print("Thread_save_print_Thread.run method unexpected error: " + str(e))
            time.sleep(0.5)
        self.work = False
        print("Thread_save_print_Thread run method is ended.")

        
    def Start_run(self):
        print("Thread_save_print_Thread run method is starting.")
        self.work = True
        self.start()
        time.sleep(0.7)

        
    def Stop_run(self):
        print("Thread_save_print_Thread run method is ending.")
        self.work = False
        time.sleep(0.7)
        

        
            
            
