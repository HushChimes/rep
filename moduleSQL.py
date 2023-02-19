import psycopg2
from psycopg2 import OperationalError
from sqlalchemy import create_engine


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
      #   print("Успешное соединение с БД")
    except OperationalError as e:
        print(f"Произошла ошибка '{e}'")
    return connection


connection = create_connection(
    "data", "postgres", "", "127.0.0.1", "5432"
)


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def base():
    engine = create_engine(
        "postgresql+psycopg2://postgres:@localhost:5432/data")
    return engine
