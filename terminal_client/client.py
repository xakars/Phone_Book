import sys
from mode_verb import MODE_VERB, Verb_Request
from protocol_rules import PhoneBook 



class NotSpecifiedIPOrPortError(Exception):
    """Error that occurs when there is not Server or Port"""
    pass

class CanNotParseResponseError(Exception):
     """Error that occurs when we can not parse some strange 
     response from RKSOK server."""
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
    
    client = PhoneBook(server, port)
    verb = MODE_VERB.get(get_mode())
    client.set_verb(verb)
    client.set_name(input("Введите имя:"))
    if verb == Verb_Request.WRITE:
        client.set_phone(input("Введите телефон: "))
    try:
        human_readable_response = client.process()
    except CanNotParseResponseError:
        procces_critical_exeption(
                "Не понял ответ от сервера"
                )
    print(f"\nЗапрос: {client.get_raw_request()!r}\n"
          f"Ответ:{client.get_raw_response()!r}\n")
    print(human_readable_response)
    

if __name__ == "__main__":
    client_run()
