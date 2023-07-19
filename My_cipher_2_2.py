# pip install pycryptodomex
# python -m Cryptodome.SelfTest

#https://nitratine.net/blog/post/python-encryption-and-decryption-with-pycryptodome/

import os, sys
from Cryptodome.Cipher import AES
import hashlib
import base64
import random
from random import randint
from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit, QMessageBox


class My_cipher(object):

    def __init__(self, password = ""):
        self.key = None
        if password == "":
            password, ok = QInputDialog.getText(None, "My_cipher", "Enter the password: ", QLineEdit.Password)
        if password:
            self.iv = hashlib.md5(password.encode('utf-8')).digest()
            self.key = hashlib.sha256(password.encode('utf-8')).digest()


    def encrypt_bytes(self, bytes_to_encrypt):
        if self.key is not None:
            _cipher = AES.new(self.key, AES.MODE_OFB, self.iv)
            return base64.b64encode(_cipher.encrypt(bytes_to_encrypt))
        else:
            QMessageBox.about(None, "My_cipher", "ERROR - there is no password entered.")


    def decrypt_bytes(self, bytes_to_decrypt):
        if self.key is not None:
            _cipher = AES.new(self.key, AES.MODE_OFB, self.iv)
            return _cipher.decrypt(base64.b64decode(bytes_to_decrypt))
        else:
            QMessageBox.about(None, "My_cipher", "ERROR - there is no password entered.")
        

    def encrypt_string(self, text):
        if self.key is not None:
            random.seed()
            _len = random.randint(8, 14)
            if len(text) < _len:
                text.rjust(_len)
            if len(text) % 16 != 0:
                text_to_encrypt = text.rjust((len(text) // 16 + 1) * 16)
            else:
                text_to_encrypt = text
            return self.encrypt_bytes(text_to_encrypt.encode('utf-8'))
        else:
            QMessageBox.about(None, "My_cipher", "ERROR - there is no password entered.")


    def decrypt_string(self, bytes_to_decrypt):
        if self.key is not None:
            return self.decrypt_bytes(bytes_to_decrypt).strip().decode('utf-8')
        else:
            QMessageBox.about(None, "My_cipher", "ERROR - there is no password entered.")


    def encrypt_file(self, input_file_path, output_file_path):
        if self.key is not None:
            input_file = open(input_file_path, "rb")
            plain_bytes = input_file.read()
            input_file.close()
            encrypted_bytes = self.encrypt_bytes(plain_bytes)
            output_file = open(output_file_path, "wb")
            output_file.write(encrypted_bytes)
            output_file.close()
        else:
            QMessageBox.about(None, "My_cipher", "ERROR - there is no password entered.")


    def decrypt_file(self, input_file_path, output_file_path):
        if self.key is not None:
            input_file = open(input_file_path, "rb")
            encrypted_bytes = input_file.read()
            input_file.close()
            plain_bytes = self.decrypt_bytes(encrypted_bytes)
            output_file = open(output_file_path, "wb")
            output_file.write(plain_bytes)
            output_file.close()
        else:
            QMessageBox.about(None, "My_cipher", "ERROR - there is no password entered.")


    def encrypt_file_and_remove_it(self, input_file_path, output_file_path):
        if self.key is not None:
            self.encrypt_file(input_file_path, output_file_path)
            os.remove(input_file_path)
        else:
            QMessageBox.about(None, "My_cipher", "ERROR - there is no password entered.")
        

    def decrypt_file_and_remove_it(self, input_file_path, output_file_path):
        if self.key is not None:
            self.decrypt_file(input_file_path, output_file_path)
            os.remove(input_file_path)
        else:
            QMessageBox.about(None, "My_cipher", "ERROR - there is no password entered.")
        

#==========================================================================================

def word_test():
    plain_text = "My_cipher test."
    my_cipher = My_cipher()
    print(plain_text)
    encrypted_text = my_cipher.encrypt_string(plain_text)
    print(encrypted_text)
    text = my_cipher.decrypt_string(encrypted_text)
    print(text)


def file_test():
    PLAIN_FILE_PATH = 'pythonsqlite.db'
    ENCRYPTED_FILE_PATH = 'pythonsqlite.mcph'
    my_cipher = My_cipher()
    #my_cipher.encrypt_file_and_remove_it(PLAIN_FILE_PATH, ENCRYPTED_FILE_PATH)
    my_cipher.decrypt_file_and_remove_it(ENCRYPTED_FILE_PATH, PLAIN_FILE_PATH)

        
#------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    word_test()
    #file_test()


