import os
from dotenv import load_dotenv
import src.services as services
import src.view as view
import src.admin as admin

load_dotenv()
db_user = os.getenv('DB_USER')
data_users = services.get(db_user)

global tmp_user
tmp_user = {}


def login(username, password):
    for user in data_users:
        if username == user['username']:
            if password == user['password']:
                return user
            else:
                return 'password salah'
    return 'user tidak ditemukan'


def list_user(data=data_users):
    view.text_in_line(liner='-')
    print(f"   {'No.':<5}{'Username':<15}{'Role':<15}")
    view.text_in_line(liner='-')
    for i, user in enumerate(data):
        print(f"   {str(i+1)+'.':<5}{user['username']:<15}{user['role']:<15}")
    view.text_in_line(liner='-')
    print()
    input('Enter untuk kembali ke Menu')
    admin.main()


def back_to_menu(key):
    if key == '0':
        admin.main()


def add_user(isBack=False):
    admin.header('Tambah User', 'Menu')
    view.text_in_line(liner='-')

    if isBack:
        print(f"   {'Username':<9} : "+tmp_user['username'])
        print(f"   {'Password':<9} : "+tmp_user['password'])
        tmp_user['role'] = input(
            f"   {'Role [A]->(Admin), [K]->(Kasir)':<9} : ").upper()
        back_to_menu(tmp_user['role'])
    else:
        tmp_user['username'] = input(f"   {'Username':<9} : ")
        back_to_menu(tmp_user['username'])

        tmp_user['password'] = input(f"   {'Password':<9} : ")
        back_to_menu(tmp_user['password'])

        tmp_user['role'] = input(
            f"   {'Role [A]->(Admin), [K]->(Kasir)':<9} : ").upper()
        back_to_menu(tmp_user['role'])

    if not tmp_user['role'].isalpha() or (tmp_user['role'] != 'A' and tmp_user['role'] != 'K'):
        print()
        view.text_in_line('Inputkan huruf A atau K', color='red')
        input()
        add_user(True)
    else:
        if tmp_user['role'] == 'A':
            tmp_user['role'] = 'admin'
        else:
            tmp_user['role'] = 'kasir'

        data_users.append(tmp_user)
        result = services.post(db_user, data_users)

        print()
        view.text_in_line(
            f"User '{result['username']}' berhasil ditambahkan", color='green')
        print()
        input('Enter untuk kembali ke Menu')
        admin.main()
