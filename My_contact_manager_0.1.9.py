SCRIPT_TITLE = 'My contact manager'
SCRIPT_VERSION = '0.1.9'
GENERAL_INFO = """
author: Piotr Michałowski, Olsztyn, woj. W-M, Poland
piotrm35@hotmail.com
license: GPL v. 2
work begin: 08.07.2019
"""

# Python 3.6.7

import os, sys, time, datetime
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Command_sender.MyLineEdit import MyLineEdit
from My_QLabel import My_QLabel
from Setup import Setup
from SQLite_manager_0_1_4 import SQLite_manager
from My_cipher_2_2 import My_cipher
from Command_sender.Command_sender_0_6_4 import Command_sender
from Contact_edit_0_1_2 import Contact_edit
from Logger import Logger


class My_contact_manager(QtWidgets.QWidget):


    def __init__(self):
        super(My_contact_manager, self).__init__()
        self.base_path = os.sep.join(os.path.realpath(__file__).split(os.sep)[0:-1])
        self.encrypted_db_file_path = os.path.join(self.base_path, 'db', Setup.ENCRYPTED_CONTACT_DB_FILE_NAME)
        self.plain_db_file_path = os.path.join(self.base_path, 'db', Setup.CONTACT_DB_FILE_NAME)
        uic.loadUi(os.path.join(self.base_path, 'ui', 'My_contact_manager.ui'), self)
        self.setWindowTitle(SCRIPT_TITLE + ' v. ' + SCRIPT_VERSION)
        # dodanie MyLineEdit (z obsługą przycisku enter)
        self.Search_lineEdit = MyLineEdit(self)
        self.Search_lineEdit.setGeometry(QtCore.QRect(9, 16, 281, 20))
        self.Search_lineEdit.setObjectName("Search_lineEdit")
        # obsługa przycisków i in.:
        self.Search_lineEdit.enter_pressed_signal.connect(self.Search_handleButton)
        self.Search_pushButton.clicked.connect(self.Search_handleButton)
        self.Help_pushButton.clicked.connect(self.Help_handleButton)
        self.About_pushButton.clicked.connect(self.About_handleButton)
        self.Clear_pushButton.clicked.connect(self.Clear_handleButton)
        self.Add_contact_pushButton.clicked.connect(self.Add_contact_handleButton)
        self.Edit_contact_pushButton.clicked.connect(self.Edit_contact_handleButton)
        self.Del_contact_pushButton.clicked.connect(self.Del_contact_handleButton)
        self.Dial_pushButton.clicked.connect(self.Dial_handleButton)
        self.On_hook_pushButton.clicked.connect(self.On_hook_handleButton)
        self.Command_sender_checkBox.stateChanged.connect(self.Command_sender_checkBox_stateChanged)
        self.Automatic_on_hook_checkBox.stateChanged.connect(self.Automatic_on_hook_checkBox_stateChanged)
        self.On_hook_pushButton.setEnabled(not self.Automatic_on_hook_checkBox.isChecked())
        # inne:
        self.previous_chosen_label_idx = None
        self.current_info_list = []
        self.visible_contact_list = []
        self.contact_edit = None
        self.DB_changing_sql_list = []
        self.my_cipher = My_cipher()
        self.logger = Logger(os.path.join(self.base_path, 'log', 'My_contact_manager.log'), 200 * 1024, 5, 'My_contact_manager')
        if not os.path.exists(self.plain_db_file_path):
            self.my_cipher.decrypt_file(self.encrypted_db_file_path, self.plain_db_file_path)
        try:
            self.sQLite_manager = SQLite_manager(self.plain_db_file_path, True)
            os.remove(self.plain_db_file_path)
        except:
            self.sQLite_manager = None
            self.command_sender = None
            self.logger.write_WARNING_log('Entered password is not correct.')
            print('\nEntered password is not correct.')
            os.remove(self.plain_db_file_path)
            return
        self.command_sender = Command_sender(self, Setup.COMMAND_SENDER_INITIAL_PORT)
        

    def closeEvent(self, event):        # overriding the method
        try:
            if self.sQLite_manager:
                self.sQLite_manager.close_connection()
                if self.DB_changing_sql_list:
                    self.my_cipher.decrypt_file_and_remove_it(self.encrypted_db_file_path, self.plain_db_file_path)
                    self.sQLite_manager = SQLite_manager(self.plain_db_file_path, False)
                    self.sQLite_manager.execute_sql_list(self.DB_changing_sql_list)
                    self.sQLite_manager.close_connection()
                    self.my_cipher.encrypt_file_and_remove_it(self.plain_db_file_path, self.encrypted_db_file_path)
            self.Search_lineEdit.enter_pressed_signal.disconnect(self.Search_handleButton)
            self.Search_pushButton.clicked.disconnect(self.Search_handleButton)
            self.Help_pushButton.clicked.disconnect(self.Help_handleButton)
            self.About_pushButton.clicked.disconnect(self.About_handleButton)
            self.Clear_pushButton.clicked.disconnect(self.Clear_handleButton)
            self.Add_contact_pushButton.clicked.disconnect(self.Add_contact_handleButton)
            self.Edit_contact_pushButton.clicked.disconnect(self.Edit_contact_handleButton)
            self.Del_contact_pushButton.clicked.disconnect(self.Del_contact_handleButton)
            self.Dial_pushButton.clicked.disconnect(self.Dial_handleButton)
            self.On_hook_pushButton.clicked.disconnect(self.On_hook_handleButton)
            self.Command_sender_checkBox.stateChanged.disconnect(self.Command_sender_checkBox_stateChanged)
            self.Automatic_on_hook_checkBox.stateChanged.disconnect(self.Automatic_on_hook_checkBox_stateChanged)
        except Exception as e:
            self.logger.write_WARNING_log('closeEvent exception: ' + str(e))
            print('closeEvent exception: ' + str(e))
        event.accept()
        

    #----------------------------------------------------------------------------------------------------------------


    def Search_handleButton(self):
        if self.sQLite_manager:
            self.Search_pushButton.setEnabled(False)
            self._ordinary_cleaning()
            tx = str(self.Search_lineEdit.text())
            pn = self._get_phone_number(tx)
            if pn is not None:
                tx = pn
            self.visible_contact_list = self.sQLite_manager.select_contact_by_pattern(tx)
            self._show_contacts()
            self.Search_pushButton.setEnabled(True)
        

    def Help_handleButton(self):
        help_message = """Wybierz (wyświetl) kontakty za pomocą narzędzia [serch].\n
Kliknij kontakt, a następnie w oknie info (na dole)\n
wstaw kursor w obrębie numeru telefonu i naciśnij przycisk [dial]."""
        QtWidgets.QMessageBox.information(self, SCRIPT_TITLE, help_message)
        

    def About_handleButton(self):
        QtWidgets.QMessageBox.information(self, SCRIPT_TITLE, SCRIPT_TITLE + ' v. ' + SCRIPT_VERSION + '\n' + GENERAL_INFO)
        

    def Clear_handleButton(self):
        self._ordinary_cleaning()
        self.Search_lineEdit.clear()

        
    def Add_contact_handleButton(self):
        if self.sQLite_manager:
            self.contact_edit = Contact_edit(self)
            self.contact_edit.show()


    def Edit_contact_handleButton(self):
        if self.sQLite_manager and self.previous_chosen_label_idx is not None:
            self.contact_edit = Contact_edit(self, self.visible_contact_list[self.previous_chosen_label_idx])
            self.contact_edit.show()


    def Del_contact_handleButton(self):
        if self.sQLite_manager and self.current_info_list:
            button_reply = QtWidgets.QMessageBox.question(self, SCRIPT_TITLE, "Delete contact?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if button_reply == QtWidgets.QMessageBox.Yes:
                sql = self.sQLite_manager.delete_contact(self.current_info_list[0])
                self.DB_changing_sql_list.append(sql)
##                self.logger.write_INFO_log('sql = ' + str(sql))
                self.Search_handleButton()
        

    def Dial_handleButton(self):
        if self.sQLite_manager and self.current_info_list:
            self.Dial_pushButton.setEnabled(False)
            cursor_position = int(self.Info_textEdit.textCursor().position())
            t = 0
            for r in range(len(self.current_info_list)):
                t += len(self.current_info_list[r]) + 1         # + 1 bo + '\n'
                if cursor_position < t:
                    phone_number = self._get_phone_number(self.current_info_list[r])
                    self.command_sender.Send_command('ATDT' + Setup.DIAL_PREFIX + phone_number + ';')
                    if self.Automatic_on_hook_checkBox.isChecked():
                        time.sleep(3.0)
                        self.command_sender.Send_command('ATH0')
                    self.logger.write_INFO_log('dial ' + phone_number)
                    break
            self.Dial_pushButton.setEnabled(True)


    def On_hook_handleButton(self):
        self.On_hook_pushButton.setEnabled(False)
        self.command_sender.Send_command('ATH0')
        self.On_hook_pushButton.setEnabled(True)


    def Command_sender_checkBox_stateChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.command_sender.show()
        else:
            self.command_sender.hide()


    def Automatic_on_hook_checkBox_stateChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.On_hook_pushButton.setEnabled(False)
        else:
            self.On_hook_pushButton.setEnabled(True)
            

    def Command_sender_is_hiding(self):
        self.Command_sender_checkBox.setChecked(False)


    def set_QLabel_as_chosen(self, idx):
        if self.Search_pushButton.isEnabled():
            self.current_info_list = []
            info = ''
            if self.previous_chosen_label_idx is not None:
                chosen_label = self.gridLayout.itemAt(self.previous_chosen_label_idx).widget()
                chosen_label.setStyleSheet('background-color: lightGray')
            chosen_label = self.gridLayout.itemAt(idx).widget()
            chosen_label.setStyleSheet('background-color: gray')
            self.previous_chosen_label_idx = idx
            for i in range(len(self.visible_contact_list[idx])):
                if i == 3:
                    phone_number_list = self.visible_contact_list[idx][i].split(';')
                    for pn in phone_number_list:
                        formated_phone_number = self._get_formated_phone_number(pn)
                        info += formated_phone_number + '\n'
                        self.current_info_list.append(formated_phone_number)
                else:
                    info += str(self.visible_contact_list[idx][i]) + '\n'
                    self.current_info_list.append(str(self.visible_contact_list[idx][i]))
            self.Info_textEdit.setText(info)
    


    #----------------------------------------------------------------------------------------------------------------


    def _ordinary_cleaning(self):
        self._remove_widgets_from_gridLayout()
        self.Info_textEdit.clear()
        self.previous_chosen_label_idx = None
        self.current_info_list = []
        self.visible_contact_list = []


    def _show_contacts(self):
        if self.visible_contact_list and len(self.visible_contact_list) > 0:
            # resize gridLayoutWidget
            gridLayoutWidget_new_width = (Setup.LABEL_WIDTH + Setup.LABEL_MARGIN * 2)
            gridLayoutWidget_new_height = (Setup.LABEL_HEIGHT + Setup.LABEL_MARGIN * 2) * len(self.visible_contact_list)
            self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, gridLayoutWidget_new_width, gridLayoutWidget_new_height))
            self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, gridLayoutWidget_new_width, gridLayoutWidget_new_height))
            # add labels
            for r in range(len(self.visible_contact_list)):
                self.gridLayout.addWidget(self._get_QLabel(r, self.visible_contact_list[r][1]), r, 0)


    def _get_QLabel(self, idx, text):
        tmp_label = My_QLabel(self, idx)
        tmp_label.setText(text)
        tmp_label.setStyleSheet('background-color: lightGray')
        tmp_label.setGeometry(QtCore.QRect(Setup.LABEL_MARGIN, Setup.LABEL_MARGIN, Setup.LABEL_WIDTH, Setup.LABEL_HEIGHT))
        tmp_label.setMinimumSize(Setup.LABEL_WIDTH, Setup.LABEL_HEIGHT)
        tmp_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        return tmp_label


    def _remove_widgets_from_gridLayout(self):
        for i in reversed(range(self.gridLayout.count())):
            widget_to_remove = self.gridLayout.itemAt(i).widget()
            self.gridLayout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)
            del widget_to_remove


    def _get_phone_number(self, tx):
        n = -1
        while n != len(tx):
            tx = tx.replace(' ', '')
            tx = tx.replace('-', '')
            tx = tx.replace('(', '')
            tx = tx.replace(')', '')
            n = len(tx)
        if tx[0:1] == '0':
            tx = tx[1:]
        try:
            i = int(tx)
            return tx
        except:
            return None


    def _get_formated_phone_number(self, input_pn):
        pn = self._get_phone_number(input_pn)
        if pn is None:
            return input_pn
        if pn is None or len(pn) != 9:
            return pn
        if pn[0:2] in Setup.KNOWN_PHONE_NUMBER_PREFIXES:
            return pn[0:2] + ' ' + pn[2:5] + '-' + pn[5:7] + '-' + pn[7:]
        else:
            return pn[0:3] + '-' + pn[3:6] + '-' + pn[6:]
        

#====================================================================================================================

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_contact_manager = My_contact_manager()
    my_contact_manager.show()
    sys.exit(app.exec_())


