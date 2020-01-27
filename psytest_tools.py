###########################################################
#                                                         #
#              Автор: Владислав Faralaks                  #
#                 Специально для МГППУ                    #
#                                                         #
###########################################################

from bson.objectid import ObjectId as obj_id
from string import ascii_letters, digits
from application import mongo_connect
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

# Функции шифрования, дешифрования (ECB AES) и генерации паролей
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


def gen_pass(leng=8, alf=ascii_letters + digits*2):
    """Генерерует простой пароль заданной длины из заданного алфавита."""
    pas = ''
    for _ in range(leng):
        pas += alf[randint(0, len(alf)-1)]
    return pas

# Функция проверики сессии
def check_session(status, ses):
    """Проверяет, активна ли сессия и доступна ли ему эта страница."""
    try:
        users = mongo_connect.db.users
        real_user = users.find_one({'_id':obj_id(ses['_id']),'$or':[{'pre_del':None}, {'pre_del':{'$gt':now_stamp()}}]},
                {'_id':0,'status':1, 'login':1, 'pas':1})
        if real_user:
            if (now() < ses['timeout'] and
                    real_user['status'] == status and
                    real_user['login'] == ses['login'] and
                    real_user['pas'] == ses['pas']):
                return True
        return False
    except: 
        return False

# Полезный заметный принт
def vprint(*items):
    """Принимает >= 1 объект, принтит их один за другим для удобного просмотра"""
    print('\n-----------------------\n')
    for i in items:
        print('\t', i)
    print('\n-----------------------\n')

# Функции для работы с коллекцией юзеров
def remake_users(yes='no'):
    """Принимает "yes" как подтверждение очистки. Очищает коллекцию юзеров, возводит идексы"""
    if yes == "yes":
        users = mongo_connect.db.users
        users.delete_many({})
        users.create_index('login', unique=True)  
        users.create_index('ident', unique=True, sparse=True) 
    else: raise Exception("В качестве подтверждения удаления, добавьте \"yes\" первым параметром")


def add_psy(login, pas, ident, tests, count, added_by):
    """Принимает логин, пароль, идентификатор, [тесты], доступное кол-во испытуемых, логин создателя. 
    добавляет нового психолого в коллекию юзеров. возвращает его уникальный _id объект"""
    users = mongo_connect.db.users
    user_id = users.insert_one({'login':str(login).capitalize(), 'pas': encrypt(str(pas)), 'ident':str(ident), 'added_by':added_by, 'tests':tests,
            'count':int(count), 'status':'psy', 'counter':0, 'create_date':now_stamp(), 'pre_del':None}).inserted_id
    return user_id

def add_testees(counter, count, login, grade, tests, added_by, current):
    """Принимает логин, пароль, идентификатор, тесты, доступное кол-во, логин создателя. 
    добавляет нового психолого в коллекию юзеров. возвращает его уникальный _id объект"""
    users = mongo_connect.db.users
    insert_testees = []
    for i in range(counter, counter+count):
        insert_testees.append({'login':login.capitalize()+str(i), 'tests':tests, 'grade':str(grade).upper(),
        'pas':encrypt(gen_pass(12)), 'added_by':obj_id(added_by),
        'status':'testee', 'result':'Тестируется', 'pre_del':None, 'create_date':now_stamp()})
    users.insert_many(insert_testees)
    users.update_one({'_id':obj_id(added_by)}, {'$set':{'counter':counter+count, 'count':current-count}})
    return

def get_all_psys():
    """Возвращает список всех псизологов"""
    users = mongo_connect.db.users
    return users.find({'status':'psy', '$or':[{'pre_del':None}, {'pre_del':{'$gt':now_stamp()}}]},
                {'login':1, 'pas':1, 'create_date':1, 'pre_del':1, 'ident':1, 'count':1, 'tests':1})

def get_testees(added_by):
    """Принимает логин психолога, добавившего испытуемых. Возвращает список всех испытуемых этого психолога"""
    users = mongo_connect.db.users
    return users.find({'status':'testee', 'added_by':str(added_by), 'pre_del':None},
                {'result':1,'login':1, 'pas':1, 'grade':1, 'tests':1, 'create_date':1})

def get_user(login):
    """Принимает логин пользователшя, возвращает его данные в словаре, если такого пользователя нет
    или подошел срок удаления, функция возвращает None"""
    users = mongo_connect.db.users
    user_data = users.find_one({'login':str(login), '$or':[{'pre_del':None}, {'pre_del':{'$gt':now_stamp()}}]})
    return user_data


def update_psy(user_id, login, pas, tests, count, ident, pre_del):
    """Принимает уникальный _id психолога, новый логин, новый пароль, список новых тестов, новое доступное кол-во испытуемых,
    новый идентификатор, новое значение предварительного удаления. Обновляет данные у данного психолога"""
    users = mongo_connect.db.users
    users.update_one({'_id':obj_id(_id)}, {'$set':{'login':str(login).capitalize(), 'pas':encrypt(str(pas)),
        'tests':tests, 'count':int(count), 'ident':str(ident), 'pre_del':pre_del}})



def insert(col, **dock):
    return users.insert_one(dock).inserted_id
def update_user(col, _id, **new):
    users.update_one({'_id':obj_id(_id)}, { "$set":new})


result_code = {'1': ['Любит печенье', 'Не любит печенье'],
            '2': ['Любит изюм', 'Не любит изюм']
            }
