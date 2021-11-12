import psycopg2
from config import host, user, password, db_name

#connect to exist database
connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
)

connection.autocommit = True

def write_new_name(data):
    """Function takes request and writes values(name and phone number) to the database"""
    data_list = data.decode().split()
    name_user = " ".join(data_list[1:data_list.index('РКСОК/1.0')])
    phone = "".join(data_list[data_list.index('РКСОК/1.0')+1:])
    with connection.cursor() as cursor:
        query = "INSERT INTO users(name, phone_number) VALUES (%s, %s);"
        data = (name_user, phone)
        cursor.execute(query, data)

def find_name(data) -> str:
    """Function finds and returns existing values from database"""
    data_list = data.decode().split()
    name_user = " ".join(data_list[1:data_list.index('РКСОК/1.0')])
    with connection.cursor() as cursor:
        query = "SELECT phone_number FROM users WHERE name=%s ORDER BY id DESC"
        data = (name_user,)
        cursor.execute(query, data)
        result = cursor.fetchone()
        if result == None:
            return "НИНАШОЛ РКСОК/1.0"
        else:
            return f"НОРМАЛДЫКС РКСОК/1.0\r\n{','.join(result)}"

def delete_name(data):
    """Function removes values from database"""
    data_list = data.decode().split()
    name_user = " ".join(data_list[1:data_list.index('РКСОК/1.0')])
    with connection.cursor() as cursor:
        query = "DELETE FROM users WHERE name=%s"
        data = (name_user,)
        cursor.execute(query, data)


