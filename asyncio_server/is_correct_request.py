

def check_request(data_req: bytes) -> bool:
    """Return 'True' if client request fit the protocol else 'False'"""
    decoded_list = data_req.decode().split()
    if b'\r\n\r\n' in data_req and (decoded_list[0]=='ЗОПИШИ' or decoded_list[0]=='ОТДОВАЙ' or decoded_list[0]=='УДОЛИ') and 'РКСОК/1.0' in decoded_list:
        return True
    else:
        return False

