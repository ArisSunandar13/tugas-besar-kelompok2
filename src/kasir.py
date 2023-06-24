import src.view as view
import src.services as services


def main():
    global user
    user = services.get_last_log_history()
    
    menu_kasir = ['List & Search Produk', 'List & Search Transaksi', 'Tambah Transaksi']

    header('Menu Kasir', 'Login')
    view.print_menu(menu_kasir)
    
    key = input(f"   Pilih Menu : ")


def header(title, backto):
    view.header('KASIR')
    view.text_in_line(f"Selamat datang '{user['username']}'!", align='left')
    view.text_in_line(f"0 untuk kembali ke {backto}", align='right')
    view.text_in_line(title)
