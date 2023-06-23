import shutil
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def text_in_line(text='', liner=' ', color='', isBlink=False, align='middle'):
    terminal_length = shutil.get_terminal_size().columns - 2
    text_length = text.__len__()
    terminal_minus_text_length = terminal_length - text_length
    left_length = int(terminal_minus_text_length / 2)
    right_length = int(terminal_minus_text_length / 2)
    ansi_blink = ''
    ansi_color = ''
    ansi_start = ''
    ansi_end = ''

    if (left_length + right_length) != terminal_minus_text_length:
        left_length += 1

    if text != '':
        text = ' ' + text + ' '
    else:
        text = liner * 2

    if isBlink:
        ansi_blink = '\033[5m'
    if color == 'red':
        ansi_color = '\033[31m'
    if color == 'green':
        ansi_color = '\033[32m'
    if color == 'yellow':
        ansi_color = '\033[33m'

    if color != '' or isBlink:
        ansi_start = ansi_color + ansi_blink
        ansi_end = '\033[0m'

    text = ansi_start + text + ansi_end

    if align == 'left':
        print(text + liner * left_length + liner * right_length)
    if align == 'right':
        print(liner * left_length + liner * right_length + text)
    if align == 'middle':
        print(liner * left_length + text + liner * right_length)


def header(title='', color=''):
    clear_screen()
    text_in_line(liner='=')
    text_in_line('WARUNK MAMA FADIL', '~', 'green', True)

    if title:
        text_in_line(title, '~')

    text_in_line(liner='=')
    print()


def num_to_char(num):
    return chr(65 + num)


def print_menu(list1, list2=[], list3=[], start=0):
    text_in_line(liner='-')
    print(f"   {'KEY':<7}{'ACTIONS'}")
    text_in_line(liner='-')
    for i, text in enumerate(list1 + list2 + list3):
        if list1.__len__() == i:
            print()
        if list2.__len__() != 0 and list2.__len__() + list1.__len__() == i:
            print()

        print(f"   {num_to_char(i)+'.':<7}{text}")

    text_in_line(liner='-')
    print()


def format_rupiah(data):
    return 'Rp.{:,}'.format(int(data)).replace(',', '.')
