import src.view as view
import src.service_user as service_user
import src.admin as admin
import src.services as services
import src.kasir as kasir


def main():
    view.header()
    view.text_in_line('login', '~')
    print()

    # username = input('   Username : ')
    # password = input('   Password : ')
    # print()

    # user = service_user.login(username, password)
    # user = service_user.login('admin', 'admin123')
    user = service_user.login('kasir','kasir123')

    if type(user) == str:
        view.text_in_line(user, color='red')
        input()
        main()

    elif user['role'] == 'admin':
        services.post_log_history(user, 'Login')
        admin.main()

    elif user['role'] == 'kasir':
        services.post_log_history(user, 'Login')
        kasir.main()
