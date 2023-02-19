import shutil
from os import path
import pandas as pd
import moduleSQL


def create_query(file, nameTable):
    data = pd.read_excel(file)
    engine = moduleSQL.base()
    try:
        data.to_sql(nameTable, engine, if_exists='replace', index=False)
        print(f"Файл {nameTable} успешно записан в БД")
        new_location = shutil.move(file, "processedFiles")
    except:
        print("Ошибка записи XLSX файла")
    finally:
        engine.dispose()
