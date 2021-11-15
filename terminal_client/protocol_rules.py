import socket
from mode_verb import Verb_Request



class PhoneBook:
    """phonebook works with server arsxak.ru:80"""
    def __init__(self, server: str, port: int):
        self._server, self._port = server, port
        self._conn = None
        self._name, self._phone, self._verb = None, None, None
        self._raw_request, self._raw_response = None, None
    
    def set_name(self, name: str) -> None:
        self._name = name

    def set_phone(self, phone: str) -> None:
        self._phone = phone

    def set_verb(self, verb: Verb_Request) -> None:
        self._verb = verb
        
