import src.view as view
import src.services as services
import src.login as login
import src.service_product as service_product
import src.service_transaction as service_transaction
from dotenv import load_dotenv
import os

load_dotenv()
db_product = os.getenv('DB_PRODUCT')
db_transaction = os.getenv('DB_TRANSACTION')


def main():
    global user
    user = services.get_last_log_history()

    menu_kasir = ['List & Search Produk',
                  'List & Search Transaksi', 'Tambah Transaksi']

    header('Menu Kasir', 'Login')
    view.print_menu(menu_kasir)

    key = input(f"   Pilih Menu : ").upper()
    # key = 'C'
    if key == '0':
        login.main()

    if key.__len__() == 0:
        main()

    if not key.isalpha():
        print()
        view.text_in_line('Inputkan sebuah huruf. Contoh : A')
        print()
        input('Enter untuk lanjut')
        main()
    else:
        if key == 'A':
            service_product.list_product(data=services.get(
                db_product), isKasir=True, isSearch=True)
        if key == 'B':
            service_transaction.list_transaction(
                data=services.get(db_transaction), isKasir=True)
        if key == 'C':
            service_transaction.add_transaction(user)
        else:
            print()
            view.text_in_line(f"'{key}' tidak terdaftar", color='red')
            print()
            input('Enter untuk lanjut')
            main()


def header(title, backto):
    view.header('KASIR')
    view.text_in_line(f"Selamat datang '{user['username']}'!", align='left')
    view.text_in_line(f"0 untuk kembali ke {backto}", align='right')
    view.text_in_line(title)
