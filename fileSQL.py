import shutil
from os import path
import locale
import io
import textwrap
from psycopg2 import OperationalError, Error
import moduleSQL


def guess_encoding(file):
    with io.open(file, "rb") as f:
        data = f.read(5)
    if data.startswith(b"\xEF\xBB\xBF"):
        return "utf-8-sig"
    elif data.startswith(b"\xFF\xFE") or data.startswith(b"\xFE\xFF"):
        return "utf-16"
    else:
        try:
            with io.open(file, encoding="utf-8") as f:
                return "utf-8"
        except:
            return locale.getdefaultlocale()[1]


def create_query_string(sql_file, fileName):
    with open(sql_file, 'r', encoding=guess_encoding(sql_file)) as f_in:
        lines = f_in.read()
        query_string = textwrap.dedent("""{}""".format(lines))
        try:
            connection = moduleSQL.connection
            cursor = connection.cursor()
            cursor.execute(query_string)
            connection.commit()
            print(f"Файл {fileName} успешно записан в БД")
            f_in.close()
            new_location=shutil.move(sql_file,"processedFiles")
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
        connection.close()
        return 1