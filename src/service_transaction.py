import src.admin as admin
from dotenv import load_dotenv
import os
import src.services as services
import src.view as view
from fuzzywuzzy import fuzz
import src.kasir as kasir
import src.service_product as service_product
from datetime import datetime

load_dotenv()
db_transaction = os.getenv('DB_TRANSACTION')
db_product = os.getenv('DB_PRODUCT')

all_data_transaction = services.get(db_transaction)
all_data_product = services.get(db_product)

global user
global selected_products
global count_products
selected_products = []
count_products = []


def list_transaction(data=all_data_transaction, isKasir=False):
    if isKasir:
        kasir.header('List Transaction', 'Menu')
    if not isKasir:
        admin.header('List Transaction', 'Menu')

    view.text_in_line(liner='*')
    print(f"   {'No.':<5}{'User':<12}{'Produk':<12}{'Harga':<12}{'Jumlah':<10}{'Subtotal':<12}{'Total':<12}{'Bayar':<12}{'Kembali':<12}")
    view.text_in_line(liner='*')
    for i, item in enumerate(data):
        print(
            f"   {str(i+1)+'.':<5}{item['username']:<12}{' ':<46}{view.format_rupiah(item['total']):<12}{view.format_rupiah(item['pay']):<12}{view.format_rupiah(item['cashback']):<12}")
        for index, product in enumerate(item['products']):
            print(
                f"   {' ':<5}{' ':<12}{product['name']:<12}{view.format_rupiah(product['price']):<12}{product['quantity']:<10}{view.format_rupiah(str(int(product['price'])*int(product['quantity']))):<12}")
        if i+1 == data.__len__():
            view.text_in_line(liner='*')
        else:
            view.text_in_line(liner='-')
    print()

    result = search_transaction(data, isKasir=isKasir)
    list_transaction(result, isKasir=isKasir)


def search_transaction(data=all_data_transaction, isKasir=False):
    ratio = 90
    found_transaction = []
    view.text_in_line('Enter untuk refresh list transaction', align='right')
    key = input('   Cari Transaksi [Produk] : ')
    if key == '0' and not isKasir:
        admin.main()
    if key == '0' and isKasir:
        kasir.main()
    elif key.__len__() == 0:
        list_transaction(isKasir=isKasir)
    else:
        for item in data:
            for product in item['products']:
                if fuzz.partial_ratio(product['name'].lower(), key.lower()) >= ratio:
                    found_transaction.append(item)

    return found_transaction


def add_transaction(data_user, data_product={}, isRecall=False):
    user = data_user

    kasir.header('Tambah Transaksi', 'Menu')

    if not isRecall:
        if data_product.__len__() == 0:
            service_product.list_product(isKasir=True, data_user=data_user)
        else:
            selected_products.append(data_product)

    if selected_products.__len__() > 0:
        service_product.list_product(
            [selected_products[-1]], False, False, True, True)

    count = input('   Banyaknya : ')
    if count.__len__() == 0:
        add_transaction(data_user, isRecall=True)
    if count.isnumeric():
        if int(count) > int(selected_products[-1]['quantity']):
            print()
            view.text_in_line(
                f"Stok produk tersisa {selected_products[-1]['quantity']}", color='red')
            print()
            input('Enter untuk lanjut')
            add_transaction(data_user, isRecall=True)
        else:
            count_products.append(count)
    else:
        print()
        view.text_in_line(f"'{count}' tidak valid", color='red')
        view.text_in_line('Input yang diperbolehkan hanya angka', color='red')
        print()
        input('Enter untuk lanjut')
        add_transaction(data_user, isRecall=True)

    kasir.header('Tambah Transaksi', 'Menu')
    list_product_transaction(selected_products)

    again = input('   Lagi? [y/n] : ').upper()
    if again == 'Y' or again == 'N':
        if again == 'Y':
            add_transaction(data_user)
        if again == 'N':
            pay = check_pay(selected_products)
            kasir.header('Tambah Transaksi', 'Menu')
            list_product_transaction(selected_products, pay)

            post_transaction(data_user, pay)
    else:
        again = input('   Lagi? [y/n]')


def list_product_transaction(data, pay=0):
    total = 0
    view.text_in_line(liner='-')
    print(
        f"   {'No.':<5}{'Nama':<25}{'Harga':<15}{'Stok':<10}{'Jumlah':<10}{'Sub Total':<15}")
    view.text_in_line(liner='-')
    for i, product in enumerate(data):
        subtotal = int(product['price'])*int(count_products[i])
        total += subtotal
        if (i+1) % 6 == 0:
            print()
        print(
            f"   {str(i+1)+'.':<5}{product['name']:<25}{view.format_rupiah(product['price']):<15}{product['quantity']:<10}{count_products[i]:<10}{view.format_rupiah(str(subtotal)):<15}")
    view.text_in_line(liner='-')
    if pay > 0:
        print(f"   {' ':<55}{'BAYAR':<8}{':':<2}{view.format_rupiah(str(pay))}")
    print(f"   {' ':<55}{'TOTAL':<8}{':':<2}{view.format_rupiah(str(total))}")
    if pay > 0:
        print(
            f"   {' ':<55}{'KEMBALI':<8}{':':<2}{view.format_rupiah(str(pay-total))}")

    return total


def check_pay(selected_products):
    kasir.header('Tambah Transaksi', 'Menu')
    total = list_product_transaction(selected_products)
    pay = input('   Bayar : ')
    if pay.isnumeric():
        if int(pay) < total:
            print()
            view.text_in_line('Kurang', color='red')
            print()
            input('Enter untuk lanjut')
            check_pay(selected_products)
        else:
            return int(pay)
    else:
        print()
        view.text_in_line('Input tidak valid', color='red')
        print()
        input('Enter untuk lanjut')
        check_pay(selected_products)


def post_transaction(user, pay):
    username = user['username']
    total = 0
    pay = int(pay)

    for i, item in enumerate(selected_products):
        selected_products[i]['quantity'] = count_products[i]
        total += (int(item['price']) * int(item['quantity']))

    service_product.subtract_quantity(selected_products)

    cashback = pay - total

    data = {
        'username': username,
        'products': selected_products,
        'total': str(total),
        'pay': str(pay),
        'cashback': str(cashback),
        'date': datetime.now().strftime("%d-%m-%Y"),
        'time': datetime.now().strftime("%H:%M:%S")
    }

    data_transactions = all_data_transaction
    data_post_transaction = data_transactions + [data]

    services.post(db_transaction, data_post_transaction)

    input('Enter untuk kembali ke Menu')
    kasir.main()
