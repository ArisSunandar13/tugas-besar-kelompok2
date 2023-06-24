import src.admin as admin
from dotenv import load_dotenv
import os
import src.services as services
import src.view as view
from fuzzywuzzy import fuzz

load_dotenv()
db_transaction = os.getenv('DB_TRANSACTION')
all_data_transaction = services.get(db_transaction)


def list_transaction(data=all_data_transaction):
    admin.header('List Transaction', 'Menu')
    view.text_in_line(liner='-')
    print(f"   {'No.':<5}{'User':<15}{'Produk':<20}{'Harga':<15}{'Stok':<10}")
    view.text_in_line(liner='-')
    for i, item in enumerate(data):
        print(
            f"   {str(i+1)+'.':<5}{item['username']:<15}{item['productname']:<20}{item['price']:<15}{item['quantity']:<10}")
    view.text_in_line(liner='-')
    print()

    result = search_transaction(data)
    list_transaction(result)


def search_transaction(data=all_data_transaction):
    ratio = 90
    found_transaction = []
    key = input('   Cari Transaksi [User/Produk] : ')
    if key == '0':
        admin.main()
    elif key.__len__() == 0:
        list_transaction()
    else:
        for item in data:
            if fuzz.partial_ratio(item['username'], key) >= ratio or fuzz.partial_ratio(item['productname'], key) >= ratio:
                found_transaction.append(item)
                
    return found_transaction
