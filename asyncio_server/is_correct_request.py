

def check_request(data_req: bytes) -> bool:
    """Return True if client request fit the protocol else False"""
    decoded_list = data_req.decode().split()
    
    return data_req.endswith(b'\r\n\r\n') \
            and decoded_list[0] in ('ЗОПИШИ', 'ОТДОВАЙ', 'УДОЛИ') \
            and 'РКСОК/1.0' in decode_list

