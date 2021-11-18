import socket
from mode_verb import Verb_Request, ResponseStatus

PROTOCOL = "РКСОК/1.0"
ENCODING = "UTF-8"

HUMAN_READABLE_ANSWERS = {
        Verb_Request.GET: {
            ResponseStatus.OK: "Телефон человека {name} найден: {payload}",
            ResponseStatus.NOTFOUND: "Телефон человека {name} не найден "
            "на сервере РКСОК",
            ResponseStatus.NOT_APPROVED: "Органы проверки запретили тебе искать "
            "телефон человека {name} {payload}",
            ResponseStatus.INCORRECT_REQUEST: "Сервер не смог понять запрос на "
            "получение данных, который мы отправили."
        },
        Verb_Request.WRITE: {
            ResponseStatus.OK: "Телефон человека {name} записан",
            ResponseStatus.NOT_APPROVED: "Органы проверки запретили тебе "
            "сохранять телефон человека {name} {payload}",
            ResponseStatus.INCORRECT_REQUEST: "Сервер не смог понять запрос "
            "на запись данных, который мы отправили"
        },
        Verb_Request.DELETE: {
            ResponseStatus.OK: "Телефон человека {name} удалён",
            ResponseStatus.NOTFOUND: "Телефон человека {name} не найден на "
            "сервере РКСОК",
            ResponseStatus.NOT_APPROVED: "Органы проверки запретили тебе удалять "
            "телефон человека {name} {payload}",
            ResponseStatus.INCORRECT_REQUEST: "Сервер не смог понять запрос "
            "на удаление данных, который мы отправили"
    }
}



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

    def process(self):
        """Communication with server"""
        raw_response = self._send_request()
        human_response = self._parse_response(raw_response)
        return human_response
    
    def get_raw_request(self):
        """Returns last request in raw string format"""
        return self._raw_request
    
    def get_raw_response(self):
        """Returns last response in raw string format"""
        return self._raw_response
                    
    def _send_request(self):
        """Function sends request to server than return response"""
        request_body = self._get_request_body()
        self._raw_request = request_body.decode(ENCODING)
        if not self._conn:
            self._conn = socket.create_connection((self._server, self._port))
        self._conn.sendall(request_body)
        self._raw_response = self._receive_responce_body()
        return self._raw_response

    def _get_request_body(self) -> bytes:
        request = f"{self._verb.value} {self._name.strip()} {PROTOCOL}\r\n"
        if self._phone: request += f"{self._phone.strip()}\r\n"
        request += "\r\n"
        return request.encode(ENCODING)

    def _receive_responce_body(self) -> str:
        response = b''
        while True:
            data = self._conn.recv(1024)
            if not data: break
            response += data
        return response.decode(ENCODING)

    def _parse_response(self, raw_response: str) -> str:
        """Parses response from RKSOK server and returns parsed data"""
        for response_status in ResponseStatus:
            if raw_response.startswith(f"{response_status.value} "):
                break
        else:
            raise CanNotParseResponseError()
        response_payload = "".join(raw_response.split("\r\n")[1:])
        if response_status == ResponseStatus.NOT_APPROVED:
            response_payload = f"\nКомментарий органов: {response_payload}"
        return HUMAN_READABLE_ANSWERS.get(self._verb).get(response_status) \
                        .format(name=self._name, payload=response_payload)

