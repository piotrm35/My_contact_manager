"""
author: Piotr Michałowski, Olsztyn, woj. W-M, Poland
piotrm35@hotmail.com
license: GPL v. 2
work begin: 21.01.2019
"""

from PyQt5 import QtWidgets


class My_QLabel(QtWidgets.QLabel):
    
    def __init__(self, parent, idx):
        super(My_QLabel, self).__init__()
        self.parent = parent
        self.idx = idx

    def mouseReleaseEvent(self, e):  
        self.parent.set_QLabel_as_chosen(self.idx)
