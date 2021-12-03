import asyncio
import is_correct_request 
import is_approve
import to_db
from loguru import logger


GET = 'ОТДОВАЙ'
POST = 'ЗОПИШИ'
DELETE = 'УДОЛИ'
STATUS_OK = 'НОРМАЛДЫКС РКСОК/1.0'
STATUS_BAD_REQUEST = 'НИПОНЯЛ РКСОК/1.0'
STATUS_NOT_FOUND = 'НИНАШОЛ РКСОК/1.0'


async def listen_client(reader, writer):
    data = b''
    while True:
        global data
        tmp_data = await reader.read(1024)
        if not tmp_data or tmp_data.endswith(b'\r\n\r\n'):
            data += tmp_data
            break
        else:
            data += tmp_data
            continue
    message = data.decode()
    addr = writer.get_extra_info('peername')
    logger.info(f"Received {message!r} from {addr!r}")
    
    if is_correct_request.check_request(data):
        if is_approve.check_big_brother(data):
            if message.split()[0] == GET:
                writer.write(to_db.find_name(data).encode())
            if message.split()[0] == POST:
                to_db.write_new_name(data)
                writer.write(STATUS_OK.encode())
            if message.split()[0] == DELETE:
                if to_db.find_name(data) == STATUS_NOT_FOUND:
                    writer.write(STATUS_NOT_FOUND.encode())
                else:
                    to_db.delete_name(data)
                    writer.write(STATUS_OK.encode())
        else:
            writer.write(is_approve.check_big_brother(data))
    else:
        writer.write(STATUS_BAD_REQUEST.encode())
    await writer.drain()
    logger.info(f"Close the connection for {addr!r}" )
    data = b''
    writer.write('\r\n\r\n'.encode())
    writer.close()

async def main():
    server = await asyncio.start_server(
            listen_client, '0.0.0.0', 80) #need to keep in config('host', port)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
