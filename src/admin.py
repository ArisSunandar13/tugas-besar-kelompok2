import src.login as login
import src.view as view
import src.service_user as service_user
import src.services as services
import src.service_product as service_product
import src.service_transaction as service_transaction
from datetime import datetime


def header(title, backto):
    view.header('ADMIN')
    view.text_in_line(f"Selamat datang '{user['username']}'!", align='left')
    view.text_in_line(f"0 untuk kembali ke {backto}", align='right')
    view.text_in_line(title)


def main():
    global user
    user = services.get_last_log_history()

    menu_user = ['List User', 'Add User', 'Update User', 'Delete User']
    menu_product = ['List & Search Product',
                    'Add Product', 'Update Product', 'Delete Product']
    menu_transaction = ['List & Search Transaction']

    header('Menu Admin', 'Login')
    view.print_menu(menu_user, menu_product, menu_transaction)

    key = input('   Pilih Menu : ').upper()
    # key = 'I'

    if key == '0':
        login.main()

    if not key.isalpha():
        print()
        view.text_in_line('Inputkan sebuah huruf. Contoh : A', color='red')
        input()
        main()
    else:
        if key == 'A':
            header('List User', 'Menu')
            service_user.list_user(isBack=True)
        if key == 'B':
            service_user.add_user()
        if key == 'C':
            service_user.update_user()
        if key == 'D':
            service_user.delete_user()
        if key == 'E':
            service_product.list_product(isRecall=True)
        if key == 'F':
            service_product.add_product()
        if key == 'G':
            service_product.update_product()
        if key == 'H':
            service_product.delete_product()
        if key == 'I':
            service_transaction.list_transaction()
        else:
            print()
            view.text_in_line(f"'{key}' tidak terdaftar", color='red')
            print()
            input('Enter untuk lanjut')
            main()
