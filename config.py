from os import path, getcwd
from sys import  platform
DEBUG = True
TEMPLATES_AUTO_RELOAD = True
MONGO_URI = 'mongodb://localhost:27017/psytest_old'
SECRET_KEY = b'\xd2\x93\xc3\xb4 0\xae\x99\xf4j\x121\xd8Q2\xaa.\xaa!\x18J?@o'#+bytes(randint(1, 100)) # Ключ к секретным сессиям. Хранить в полном секрете!
DOCKS_FOLDER = path.join(getcwd(), 'docks') if platform == 'win32' or platform == 'darwin'  else '/home/flask/docks/'
NOT_YET_XLSX_TEMPLATE = path.join(getcwd(), 'not_yet_template.xlsx') if platform == 'win32' or platform == 'darwin'  else '/home/flask/not_yet_template.xlsx'