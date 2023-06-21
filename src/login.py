import src.view as view
import src.service_user as service_user
import src.admin as admin
import src.services as services

global user


def main():
    view.header()
    view.text_in_line('login', '~')
    print()

    # username = input(view.text('Username : '))
    # password = input(view.text('Password : '))
    print()

    # user = service_user.login(username, password)
    user = service_user.login('admin', 'admin123')

    if type(user) == str:
        view.text_in_line(user, color='red')
        input()
        main()

    elif user['role'] == 'admin':
        services.post_log_history({
            'username': user['username'],
            'role': user['role']
        })
        admin.main()

    elif user['role'] == 'kasir':
        # kasir.main(user)
        pass
