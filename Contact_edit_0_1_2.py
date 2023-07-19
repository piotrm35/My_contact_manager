"""
author: Piotr Michałowski, Olsztyn, woj. W-M, Poland
piotrm35@hotmail.com
license: GPL v. 2
work begin: 12.07.2019
Python 3.6.7
"""

import os
from PyQt5 import QtWidgets, uic



class Contact_edit(QtWidgets.QWidget):
    def __init__(self, parent, contact_list = None):
        super(Contact_edit, self).__init__()
        self.parent = parent
        self.base_path = os.sep.join(os.path.realpath(__file__).split(os.sep)[0:-1])
        uic.loadUi(os.path.join(self.base_path, 'ui', 'Contact_edit.ui'), self)
        self.contact_id = None
        if contact_list and (len(contact_list) == 5 or len(contact_list) == 6):
            if len(contact_list) == 6:
                self.contact_id = contact_list[0]
                contact_list = contact_list[1:]
            self.Name_textEdit.insertPlainText(contact_list[0])
            self.Address_textEdit.insertPlainText(contact_list[1])
            self.Phone_numbers_textEdit.insertPlainText(self.set_format_phone_numbers(contact_list[2]))
            self.Email_textEdit.insertPlainText(contact_list[3])
            self.Comments_textEdit.insertPlainText(contact_list[4])
        self.OK_pushButton.clicked.connect(self.OK_handleButton)


    def closeEvent(self, event):        # overriding the method
        self.OK_pushButton.clicked.disconnect(self.OK_handleButton)
        event.accept()


    def OK_handleButton(self):
        contact_list = []
        contact_list.append(self.Name_textEdit.toPlainText())
        contact_list.append(self.Address_textEdit.toPlainText())
        contact_list.append(self.remove_format_phone_numbers(self.Phone_numbers_textEdit.toPlainText()))
        contact_list.append(self.Email_textEdit.toPlainText())
        contact_list.append(self.Comments_textEdit.toPlainText())
        if self.contact_id is None:
            sql = self.parent.sQLite_manager.create_contact(contact_list)
        else:
            contact_list.append(self.contact_id)
            sql = self.parent.sQLite_manager.update_contact(contact_list)
        self.parent.DB_changing_sql_list.append(sql)
##        self.parent.logger.write_INFO_log('sql = ' + str(sql))
        self.parent.Search_handleButton()
        self.close()


    def remove_format_phone_numbers(self, raw_pn):
        raw_pn_list = raw_pn.split(';')
        pn_output = ''
        for tx in raw_pn_list:
            pn = self.parent._get_phone_number(tx)
            if len(pn_output) > 0:
                pn_output += ';'
            if pn is not None:
                pn_output += pn
            else:
                pn_output += tx
        return pn_output


    def set_format_phone_numbers(self, input_pn):
        pn_list = input_pn.split(';')
        pn_output = ''
        for pn in pn_list:
            tx = self.parent._get_formated_phone_number(pn)
            if len(pn_output) > 0:
                pn_output += '; '
            pn_output += tx
        return pn_output

