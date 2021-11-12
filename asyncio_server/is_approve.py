import socket
from typing import Union


def check_big_brother(data_req: bytes) -> Union[bool, bytes]:
    """Return 'True' if vragi-vezde.to.digital allowed request, else service response """
    first_part_req = 'АМОЖНА? РКСОК/1.0\r\n'
    conn_to_big_brother = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_to_big_brother.connect(("vragi-vezde.to.digital", 51624))
    conn_to_big_brother.send(f"{first_part_req}{data_req.decode()}".encode())
    recived = conn_to_big_brother.recv(1024)
    if recived.decode().split()[0] == 'МОЖНА':
        return True
    else:
        return recived
