
DEBUG = True
TEMPLATES_AUTO_RELOAD = True
SECRET_KEY = b'\xd2\x93\xc3\xb4 0\xae\x99\xf4j\x121\xd8Q2\xaa.\xaa!\x18J?@o'#+bytes(randint(1, 100)) # Ключ к секретным сессиям. Хранить в полном секрете!
DB_NAME = 'psytest' # Имя базы данных в MongoDB 
USERS_COL_NAME = 'users' # Имя коллекции пользователей
MONGO_ADDRESS = 'mongodb://localhost:27017/' # Адрес MongoDB