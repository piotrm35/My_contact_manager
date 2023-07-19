# -*- coding: utf-8 -*-

# Python 3.6.7


from PyQt5 import QtCore, QtWidgets

class MyLineEdit(QtWidgets.QLineEdit):

    enter_pressed_signal = QtCore.pyqtSignal()
    
    def __init__(self, *args):
        super(MyLineEdit, self).__init__(*args)
        
    def event(self, event):
        if (event.type() == QtCore.QEvent.KeyPress) and (event.key() == QtCore.Qt.Key_Enter):
            self.enter_pressed_signal.emit()
            return True
        return QtWidgets.QLineEdit.event(self, event)
