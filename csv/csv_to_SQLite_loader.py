import os
from SQLite_manager_0_1_2 import SQLite_manager


def get_phone_number(tx):
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

    
base_path = os.sep.join(os.path.realpath(__file__).split(os.sep)[0:-1])
OUTPUT_DB_FILE_PATH = os.path.join(base_path, 'db', 'pythonsqlite.db')

sQLite_manager = SQLite_manager(OUTPUT_DB_FILE_PATH)
sQLite_manager.create_contacts_table()
base_csv_folder = os.path.join(base_path, 'csv')
csv_file_names = [f for f in os.listdir(base_csv_folder) if os.path.isfile(os.path.join(base_csv_folder, f)) and os.path.splitext(f)[1].upper() == '.CSV']
for csv_file_name in csv_file_names:
    print('------------------------------------------------------------------------------------------------------------')
    print(csv_file_name + '\n')
    input_file_path = os.path.join(base_path, 'csv', csv_file_name)

    for line in open(input_file_path, 'r', encoding = 'utf8'):
        n = -1
        while n != len(line):
            line = line.replace(';;', ';')
            line = line.replace('  ', ' ')
            line = line.replace('\n', '')
            n = len(line)
        line_list = line.split(';')
        line_list = [x for x in line_list if len(x) > 1]
        print(str(line_list))
        
        if line_list and len(line_list) >= 3 and line_list[0] != 'Opis':
            contact_list = [None] * 5
            contact_list[0] = line_list[1]
            contact_list[1] = line_list[0]
            phone_numbers = ''
            email_addresses = ''
            comments = ''
            for i in range(2, len(line_list)):
                pn = get_phone_number(line_list[i])
                if pn is not None:
                    if len(phone_numbers) > 0:
                        phone_numbers += ';'
                    phone_numbers += pn
                elif '@' in line_list[i]:
                    if len(email_addresses) > 0:
                        email_addresses += ';'
                    email_addresses += line_list[i].strip()
                else:
                    if len(comments) > 0:
                        comments += ';'
                    comments += line_list[i]
            contact_list[2] = phone_numbers
            contact_list[3] = email_addresses
            contact_list[4] = comments
            id = sQLite_manager.create_contact(contact_list)
            print(str(id) + ' -> ' + str(contact_list))
            print('\n')
sQLite_manager.close_connection()
