import sys 
from enum import Enum

class NotSpecifiedIPOrPortError(Exception):
    """Error that occurs when there is not Server or Port"""
    pass

def process_critical_exception(message: str):
    """Print message about critical situation and exit"""
    print(message)
    exit(1)

def get_mode() -> int:
    """Get mode from user
    There are 3 type mode:
        1. get phone number
        2. write phone number
        3. delite phone number"""
    while True:
        mode = input(
                "Привеееет, выбери режим взаимодействия с сервером:\n"
                "1 - получить телефон пользователя\n"
                "2 - записать телефон пользователя\n"
                "3 - удалить информацию по имени\n")
        try:
            mode = int(mode)
            if not 0 < mode < 4:
                raise ValueError()
            break
        except ValueError:
            print("Что-то ввел не то, Выбери один из трех вариантов")
            continue
    return mode

def get_server_port() -> tuple[str, int]:
    "Return server and port from cmd arguments"
    try:
        return sys.argv[1], int(sys.argv[2])
    except(IndexError, ValueError):
        raise NotSpecifiedIPOrPortError()

def client_run() -> None:
    try:
        server, port = get_server_port()
    except NotSpecifiedIPOrPortError:
        process_critical_exception(
                "УПС!!! не правильно запустил.\n"
                "Запускать надо так:\n"
                "python3.10 client.py arsxak.ru 80"
                )
    print(get_mode())



if __name__ == "__main__":
    client_run()
