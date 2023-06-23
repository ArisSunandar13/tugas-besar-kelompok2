import os
from dotenv import load_dotenv
import src.services as services
import src.view as view
import src.admin as admin
from fuzzywuzzy import fuzz

load_dotenv()
db_product = os.getenv('DB_PRODUCT')
data_products = services.get(db_product)

global tmp_product
tmp_product = {}


def get_data_product():
    return data_products


def back_to_menu(key):
    if key == '0':
        admin.main()


# LIST PRODUCT
def list_product(data=get_data_product(), isSearch=True):
    admin.header('List Product', 'Menu')
    view.text_in_line(liner='-')
    print(f"   {'No.':<5}{'Nama':<25}{'Harga':<15}{'Stok':<10}")
    view.text_in_line(liner='-')
    for i, product in enumerate(data):
        print(
            f"   {str(i+1)+'.':<5}{product['name']:<25}{view.format_rupiah(product['price']):<15}{product['quantity']:<10}")
    view.text_in_line(liner='-')
    print()

    if isSearch:
        search_product()
    else:
        input('Enter untuk lanjut')
        list_product()


def search_product(data=get_data_product()):
    found_products = []
    ratio = 75

    key = input('   Cari Product [No/Nama] : ')
    back_to_menu(key)

    if key.__len__() == 0:
        list_product()
    if key.isnumeric():
        found_products.append(data[int(key)-1])
    if key.isalnum():
        for product in data:
            if fuzz.partial_ratio(key, product['name']) >= ratio:
                found_products.append(product)

    list_product(found_products, False)


# ADD PRODUCT
def add_product(data_recall={}):
    admin.header('Tambah Product', 'Menu')
    view.text_in_line(liner='-')

    if data_recall.__len__() >= 1:
        print(f"   {'Nama Produk':<15} : {data_recall['name']}")
    else:
        name = input(f"   {'Nama Produk':<15} : ")
        back_to_menu(name)
        if name.__len__() == 0:
            add_product()
        elif name.__len__() < 3:
            print()
            view.text_in_line('Nama Produk minimal 3 karakter', color='red')
            print()
            input('Enter untuk lanjut')
            add_product()
        elif name.isnumeric():
            print()
            view.text_in_line('Nama Produk tidak valid', color='red')
            print()
            input('Enter untuk lanjut')
            add_product()
        else:
            tmp_product['name'] = name

    if data_recall.__len__() >= 2:
        print(f"   {'Harga Produk':<15} : {data_recall['price']}")
    else:
        price = input(f"   {'Harga Produk':<15} : ")
        back_to_menu(price)
        if price.__len__() == 0:
            add_product(data_recall=tmp_product)
        elif price.__len__() < 3:
            print()
            view.text_in_line('Harga Produk minimal 3 karakter', color='red')
            print()
            input('Enter untuk lanjut')
            add_product(data_recall=tmp_product)
        elif not price.isnumeric():
            print()
            view.text_in_line('Harga Produk tidak valid', color='red')
            print()
            input('Enter untuk lanjut')
            add_product(data_recall=tmp_product)
        else:
            tmp_product['price'] = price

    quantity = input(f"   {'Stok Produk':<15} : ")
    back_to_menu(quantity)
    if quantity.__len__() == 0:
        add_product(data_recall=tmp_product)
    elif not quantity.isnumeric():
        print()
        view.text_in_line('Stok Produk tidak valid', color='red')
        print()
        input('Enter untuk lanjut')
        add_product(data_recall=tmp_product)
    else:
        tmp_product['quantity'] = quantity

    data = get_data_product()
    data += [tmp_product]

    result = services.post(db_product, data)

    print()
    view.text_in_line(
        f"Produk '{result['name']}' berhasil ditambahkan", color='green')
    print()
    input('Enter untuk lanjut')
    admin.main()


# UPDATE PRODUCT
def update_product(data=get_data_product()):
    input('test')


# def deleting_user(data):
    # tmp_user = data
    # get_data_users = data_users()

    # konfirm = input('   Anda yakin? [Y/N] : ').upper()

    # if konfirm != 'Y' and konfirm != 'N':
    #     print()
    #     view.text_in_line('Inputkan Y atau N')
    #     print()
    #     input('Enter untuk lanjut')

    # if konfirm == 'Y':
    #     for index, user in enumerate(get_data_users):
    #         if data == user:
    #             del get_data_users[index]
    #     services.post(db_user, get_data_users)
    #     print()
    #     view.text_in_line(
    #         f"User '{tmp_user['username']}' berhasil dihapus", color='green')
    #     print()
    #     input('Enter untuk lanjut')
    #     delete_user()

    # if konfirm == 'N':
    #     delete_user()


# DELETE USER
# def delete_user(data=data_users(), isRecall=False):
    # user_selected = []
    # ratio = 80
    # index = 0
    # key = ''

    # admin.header('Delete User', 'Menu')

    # list_user(data)

    # if isRecall:
    #     key = input('   Pilih User [No] : ')
    #     if not key.isnumeric():
    #         print()
    #         view.text_in_line(
    #             f'Pilih hanya No 1 sampai {data.__len__()}', color='red')
    #         print()
    #         input('Enter untuk lanjut')
    #         delete_user(data)
    # else:
    #     key = input('   Pilih User [No/Username] : ')
    # back_to_menu(key)

    # if key.__len__() == 0:
    #     delete_user()
    # elif key.isnumeric():
    #     deleting_user(data[int(key)-1])
    # else:
    #     for i, user in enumerate(data):
    #         if fuzz.partial_ratio(key, user['username']) >= ratio:
    #             index = i
    #             user_selected.append(user)

    #     if user_selected.__len__() == 0:
    #         print()
    #         view.text_in_line('User tidak ditemukan', color='red')
    #         print()
    #         input('Enter untuk lanjut')
    #         delete_user()
    #     elif user_selected.__len__() > 1:
    #         print()
    #         view.text_in_line('Ditemukan lebih dari 1 user', color='green')
    #         print()
    #         input('Enter untuk lanjut')
    #         delete_user(user_selected, True)
    #     else:
    #         deleting_user(index)
