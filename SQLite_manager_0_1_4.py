# http://www.sqlitetutorial.net/sqlite-python/
# https://docs.python.org/3/library/sqlite3.html


import sqlite3


class SQLite_manager:

    def __init__(self, contacts_db_file, memory_mode):
        self.db_connection = sqlite3.connect(contacts_db_file)
        self.cursor = self.db_connection.cursor()
        self.memory_mode = memory_mode
        if self.memory_mode:
            try:
                row_list = self.select_all_contacts()
            except:
                raise
            finally:
                self.db_connection.close()
            self.db_connection = sqlite3.connect(":memory:")
            self.cursor = self.db_connection.cursor()
            self.create_contacts_table()
            for row in row_list:
                self.create_contact(row)

    def __del__(self):
        self.close_connection()

    #------------------------------------------------------------------------------------------------------------------------------

    def close_connection(self):
        if self.db_connection:
            self.db_connection.close()
            
    def save_memory_db_to_file(self, contacts_db_file):
        if self.memory_mode:
            row_list = self.select_all_contacts()
            tmp_con = self.db_connection
            tmp_cur = self.cursor
            self.db_connection = sqlite3.connect(contacts_db_file)
            self.cursor = self.db_connection.cursor()
            self.create_contacts_table()
            for row in row_list:
                self.create_contact(row[1:])
            self.close_connection()
            self.db_connection = tmp_con
            self.cursor = tmp_cur
        
    #------------------------------------------------------------------------------------------------------------------------------

    def create_contacts_table(self):
        sql = """CREATE TABLE IF NOT EXISTS contacts (
                    id integer PRIMARY KEY,
                    name text NOT NULL,
                    address text,
                    phone_numbers text,
                    email text,
                    comments text
                );"""
        self.cursor.execute(sql)

    #------------------------------------------------------------------------------------------------------------------------------

    def create_contact(self, contact_list):
        if len(contact_list) == 6:
            sql = "INSERT INTO contacts (id, name, address, phone_numbers, email, comments) VALUES({0[0]}, '{0[1]}', '{0[2]}', '{0[3]}', '{0[4]}', '{0[5]}');".format(contact_list)
        elif len(contact_list) == 5:
            sql = "INSERT INTO contacts (name, address, phone_numbers, email, comments) VALUES('{0[0]}', '{0[1]}', '{0[2]}', '{0[3]}', '{0[4]}');".format(contact_list)
        else:
            return 'SQLite_manager.create_contact ERROR: ' + str(contact_list)
        self.cursor.execute(sql)
        self.db_connection.commit()
        return sql

    def update_contact(self, contact_and_id_list):
        sql = "UPDATE contacts SET name = '{0[0]}', address = '{0[1]}', phone_numbers = '{0[2]}', email = '{0[3]}', comments = '{0[4]}' WHERE id = {0[5]};".format(contact_and_id_list)
        self.cursor.execute(sql)
        self.db_connection.commit()
        return sql

    def delete_contact(self, id):
        sql = "DELETE FROM contacts WHERE id = {0};".format(id,)
        self.cursor.execute(sql)
        self.db_connection.commit()
        return sql

    def delete_all_contacts(self):
        sql = "DELETE FROM contacts;"
        self.cursor.execute(sql)
        self.db_connection.commit()
        return sql

    def execute_sql_list(self, sql_list):
        for sql in sql_list:
            if sql.startswith('INSERT') or sql.startswith('UPDATE') or sql.startswith('DELETE'):
                self.cursor.execute(sql)
                self.db_connection.commit()

    #------------------------------------------------------------------------------------------------------------------------------

    def select_contact_by_pattern(self, pattern):
        sql = "SELECT * FROM contacts WHERE name LIKE ? OR address LIKE ? OR phone_numbers LIKE ? OR email LIKE ? OR comments LIKE ?;"
        pattern_list = ('%' + pattern + '%',) * 5
        self.cursor.execute(sql, pattern_list)
        row_list = self.cursor.fetchall()
        return row_list

    def select_all_contacts(self):
        sql = "SELECT * FROM contacts;"
        self.cursor.execute(sql)
        row_list = self.cursor.fetchall()
        return row_list

#==================================================================================================================================
 
if __name__ == '__main__':
    import os
    base_path = os.sep.join(os.path.realpath(__file__).split(os.sep)[0:-1])
    DB_FILE_NAME = os.path.join(base_path, 'db', 'pythonsqlite.db')
    print(DB_FILE_NAME)

    sQLite_manager = SQLite_manager(DB_FILE_NAME, False)

##    row_list = sQLite_manager.select_all_contacts()
    row_list = sQLite_manager.select_contact_by_pattern('A+A')
    
    print('len(row_list) = ' + str(len(row_list)))
    print(str(row_list))
##    for row in row_list:
##        print(row)
    
    sQLite_manager.close_connection()
    print('SCRIPT END')
        
