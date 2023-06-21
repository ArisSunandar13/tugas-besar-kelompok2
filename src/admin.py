import src.login as login
import src.view as view
import src.service_user as service_user
import src.services as services


def header(title, backto):
    view.header('ADMIN')
    view.text_in_line(f"Selamat datang '{user['username']}'!", align='left')
    view.text_in_line(f"0 untuk kembali ke {backto}", align='right')
    view.text_in_line(title)


def main():
    global user
    user = services.get_last_log_history()

    menu_user = ['List User', 'Add User', 'Update User', 'Delete User']

    header('Menu Admin', 'Login')
    view.print_menu(menu_user)

    key = input('   Pilih Menu : ').upper()
    # key = 'B'

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
            service_user.list_user()
        if key == 'B':
            header('Tambah User', 'Menu')
            service_user.add_user()
