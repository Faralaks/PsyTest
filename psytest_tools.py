###########################################################
#                                                         #
#              Автор: Владислав Faralaks                  #
#                 Специально для МГППУ                    #
#                                                         #
###########################################################

from bson.objectid import ObjectId as obj_id
from string import ascii_letters, digits
from pymongo import MongoClient
from Crypto.Cipher import AES
from random import randint
import datetime as dt
import base64

from pprint import pprint as pp


# Функции для работы с датой
def now_stamp():
    """возвращает текущюю дату и время в формате timestamp"""
    return int(dt.datetime.now().timestamp())

def from_stamp(stamp):
    """принимает timestamp, возвращает datetime объект"""
    return dt.datetime.fromtimestamp(stamp)

def stamp2str(stamp):
    """принимает timestamp, возвращает datetime  в виде '2019-10-14 18:24:14'"""
    return str(dt.datetime.fromtimestamp(stamp))

def now():
    """returns the current datetime as datetime object"""
    return dt.datetime.now()


# Полезная функция для вывода
def vprint(*items):
    """принимает >= 1 объект, выводит из построчно для лучшей видимости среди лога"""
    print('\n-----------------------\n')
    for i in items:
        print('\t', i)
    print('\n-----------------------\n')


# Функции шифрования, дешифрования (ECB AES) и Хэширования (sha256)
def encrypt(message, passphrase=b'i1O?Tq#AhMh1?zcm?vg00wUm'):
    """принимает message и key, возвращает результат шифрования в формате base64
    ВАЖНО: key должлен быть кратен 16. 
    message будет автоматически расширен пробелами слева до длины кратной 16"""
    message = b' '* (16-(len(message) % 16)) + bytes(message, 'utf-8')
    aes = AES.new(passphrase, AES.MODE_ECB)
    return base64.b64encode(aes.encrypt(message))

def decrypt(encrypted, passphrase=b'i1O?Tq#AhMh1?zcm?vg00wUm'):
    """принимает зашифрованный message в формате base64 и key, возвращает расшифрованную строку без пробелов слева
    ВАЖНО: key должлен быть кратен 16. 
    в конце, функция lstrip используется для удаления пробелов слева от message"""
    aes = AES.new(passphrase, AES.MODE_ECB)
    return aes.decrypt(base64.b64decode(encrypted)).lstrip().decode('utf-8')

def hash(message, salt=b'JT7BX67_rVrdEpLlzWbNRV'):
    """принимает message и, опционально, соль в битовом формате, возвращает sha256 от (message + salt) с длиной 64.
    соль по умолчанию имеет длину 22"""
    return sha256(bytes(message, 'utf-8') + salt).hexdigest()

def gen_pass(leng=8, alf=ascii_letters + digits*2):
	pas = ''
	for _ in range(leng):
		pas += alf[randint(0, len(alf)-1)]
	return pas

def check_session(g, status, ses):
    '''Проверяет, активна ли сессия и открыт ли доступ, если нет, редирект на главную'''
    try:
        col = get_users_col(g) 
        count = col.count_documents({'login':ses['login'], 'pas':ses['pas'], 'pre_del':None})
        if ses['status'] == status and now() < ses['timeout'] and count != 0:
            return True
        return False
    except: return False

# Функции для работы с MongoDB
def get_db(g):
    """принимает flask.g объект, добавляет в его атрибуты объект базы, MONGO_ADDRESS,
    DB_NAME, USERS_COL_NAME (если они еще не добавлены). Возвращает объект базы"""
    db = getattr(g, 'db', None)
    if db is None:
        from config import MONGO_ADDRESS, DB_NAME, USERS_COL_NAME
        g.MONGO_ADDRESS = MONGO_ADDRESS
        g.DB_NAME = DB_NAME
        g.USERS_COL_NAME = USERS_COL_NAME
        client = MongoClient(g.MONGO_ADDRESS)
        db = g.db = client[g.DB_NAME]
    return db

def get_users_col(g):
    """принимает flask.g объект, добавляет к нему объект коллекции юзеров как арибут. возвращает объект коллекции юзеров"""
    db = get_db(g)
    users = getattr(g, 'users', None)
    if users is None:
        users = g.users = db[g.USERS_COL_NAME]
    return users


# Функции для работы с коллекцией юзеров
def remake_users(g, yes='no'):
    """принимает flask.g объект и вторым параметром "yes" как подтверждение очистки. очищает коллекцию юзеров, возводит идексы"""
    if yes == "yes":
        col = get_users_col(g)
        col.remove()
        col.create_index('login', unique=True)  
        col.create_index('ident', unique=True, sparse=True) 
    else: vprint(("в качестве подтверждения, добавьте \"да\" вторым параметром"))

def add_psy(g, login, pas, ident, tests, count, added_by):
    """принимает flask.g объект, логин, пароль, идентификатор, тесты, доступное кол-во, логин создателя. 
    добавляет нового психолого в коллекию юзеров. возвращает его уникальный _id объект"""
    col = get_users_col(g)
    _id = col.insert_one({'login':str(login).capitalize(), 'pas': encrypt(str(pas)), 'ident':str(ident), 'added_by':obj_id(added_by), 'tests':tests,
            'count':int(count), 'status':'psy', 'counter':0, 'create_date':now_stamp(), 'pre_del':None}).inserted_id
    return _id

def add_testees(g, counter, count, login, grade, tests, added_by, current):
    """принимает flask.g объект, логин, пароль, идентификатор, тесты, доступное кол-во, логин создателя. 
    добавляет нового психолого в коллекию юзеров. возвращает его уникальный _id объект"""
    col = get_users_col(g)
    insert_testees = []
    for i in range(counter, counter+count):
        insert_testees.append({'login':login.capitalize()+str(i), 'tests':tests, 'grade':str(grade).upper(),
        'pas':encrypt(gen_pass(12)), 'added_by':obj_id(added_by),
        'status':'testee', 'result':'Тестируется', 'pre_del':None, 'create_date':now_stamp()})
    col.insert_many(insert_testees)
    col.update_one({'_id':obj_id(added_by)}, {'$set':{'counter':counter+count, 'count':current-count}})
    return

def get_all_psys(g):
    """принимает flask.g объект. возвращает список всех псизологов"""
    col = get_users_col(g)
    return col.find({'status':'psy', '$or':[{'pre_del':None}, {'pre_del':{'$gt':now_stamp()}}]},
                {'login':1, 'pas':1, 'create_date':1, 'pre_del':1, 'ident':1, 'count':1, 'tests':1})

def get_testees(g, added_by_psy):
    """принимает flask.g объект, _id психолога. возвращает список всех испытуемых этого психолога"""
    col = get_users_col(g)
    return col.find({'status':'testee', 'added_by':obj_id(added_by_psy), 'pre_del':None},
                {'result':1,'login':1, 'pas':1, 'grade':1, 'tests':1, 'create_date':1,})


def get_user(g, login, pas):
    """принимает flask.g объект, login и password, возвращает данные пользователя в словаре, если такого пользователя нет
    или подошел срок удаления возвращает, False"""
    col = get_users_col(g)
    user_data = col.find_one({'login':login, '$or':[{'pre_del':None}, {'pre_del':{'$gt':now_stamp()}}]})
    if user_data != None:
        if user_data['pas'] == pas: return user_data
    return False


def update_psy(g, _id, login, pas, tests, count, ident, pre_del):
    """принимает flask.g объект, уникальный _id данного психолога, новый логин, новый пароль, список новых тестов,
    новое доступное кол-во,новый идентификатор, новое значение предварительного удаления. обновляет данные у данного психолога."""
    col = get_users_col(g)
    col.update_one({'_id':obj_id(_id)}, {'$set':{'login':str(login).capitalize(), 'pas':encrypt(str(pas)),
        'tests':tests, 'count':int(count), 'ident':str(ident), 'pre_del':pre_del}})

def get_psy_data(g, _id, ret):
    """принимает flask.g объект, уникальный _id психолога, третим параметром идет список полей, которые необходимо вернуть.
    возвращает необходимые поля данного психолога"""
    col = get_users_col(g)
    ret_dict = {}
    for i in ret: ret_dict[i] = 1
    return col.find_one({'_id':obj_id(_id), '$or':[{'pre_del':None}, {'pre_del':{'$gt':now_stamp()}}]}, ret_dict)


def insert(col, **dock):
    return col.insert_one(dock).inserted_id
def update_user(col, _id, **new):
    col.update_one({'_id':obj_id(_id)}, { "$set":new})


result_code = {'1': ['Любит печенье', 'Не любит печенье'],
            '2': ['Любит изюм', 'Не любит изюм']
            }
