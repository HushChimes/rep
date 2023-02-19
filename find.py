import os
from alive_progress import alive_bar
import time
import threading
import fileCSV
import fileSQL
import fileJSON
import fileXLSX
import fileTXT
dictFiles = {}


def main():
    global dictFiles
    dictFiles = {}
    if os.listdir('data'):
        go()
    else:
        print('Новых файлов не обнаружено, подождем')
        threading.Timer(20, main).start()


def go():
    def infoDir():
        global dictFiles
        for root, dirs, files in os.walk("data/"):
            for name in files:
                fileExtension = os.path.splitext(name)[1]
                dictFiles[fileExtension] = name
    infoDir()
    with alive_bar(len(dictFiles), title='Работа с данными', bar='bubbles') as bar:
        for fileExtension in dictFiles:
            fileName = dictFiles.get(fileExtension)
            filePath = f'data/{dictFiles.get(fileExtension)}'
            match fileExtension:
                case ".sql":
                    fileSQL.create_query_string(filePath, fileName)
                case ".csv":
                    fileCSV.create_query(filePath, fileName)
                case ".json":
                    fileJSON.create_query(filePath, fileName)
                case ".txt":
                    fileTXT.create_query(filePath, fileName)
                case ".xlsx":
                    fileXLSX.create_query(filePath, fileName)
                case Else:
                    print('Формат файлов не поддерживается')
            time.sleep(.005)
            bar()
    main()


if __name__ == "__main__":
    main()
