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

# Функции шифрования/дешифрования (ECB AES), кодирования/декодирования (base64) и генерации паролей
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

def b64enc(line: str):
    """Принимает на вход строку символов. Возвращает  base64 от этой строки"""
    return base64.b64encode(line.encode('utf-8'))

def b64dec(line: str):
    """Принимает на вход строку байт в формате base64. Возвращает  декодированну строку"""
    return base64.b64decode(line.encode('utf-8')).decode('utf-8')


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


def add_psy(login: str, pas: str, ident: str, tests: list, count: int, added_by: str):
    """Принимает логин, пароль, идентификатор, [тесты], доступное кол-во испытуемых, логин создателя. 
    добавляет нового психолого в коллекию юзеров. возвращает его уникальный _id"""
    users = mongo_connect.db.users
    user_id = users.insert_one({'login':str(login).capitalize(), 'pas': encrypt(str(pas)), 'ident':str(ident), 'added_by':str(added_by), 'tests':tests,
            'count':int(count), 'status':'psy', 'counter':0, 'create_date':now_stamp(), 'pre_del':None}).inserted_id
    return user_id

def add_testees(counter: int, count: int, ident: str, grade: str, tests: list, added_by: str, current_count: int):
    """Принимает каунтер для создания логинов испытуемых, кол-во создаваемых испытуемых,
    идентификатор психолога, который их создает, класс создаваемых испытуемых, тесты, логин создателя.
    Добавляет новых испытуемых в коллекию юзеров. возвращает список их уникальных _id."""
    users = mongo_connect.db.users
    login = str(ident).capitalize()
    grade=str(grade).upper()
    added_by = str(added_by)
    for i in range(counter, counter+count):
        users.insert_one({'login':login+'_'+str(i), 'tests':tests, 'grade':grade, 'pas':encrypt(gen_pass(10)),
                                'step':'start', 'added_by':added_by, 'status':'testee', 'result':'Нет Результата', 'pre_del':None, 'create_date':now_stamp()})
    users.update_one({'login':added_by}, {'$set':{'counter':counter+count, 'count':current_count-count}})

def get_all_psys():
    """Возвращает список всех псизологов"""
    users = mongo_connect.db.users
    return users.find({'status':'psy', '$or':[{'pre_del':None}, {'pre_del':{'$gt':now_stamp()}}]},
                {'login':1, 'pas':1, 'create_date':1, 'pre_del':1, 'ident':1, 'count':1, 'tests':1})

def get_grades_by_psy(added_by: str):
    """Принимает логин психолога, добавившего испытуемых. Возвращает список классов испытуемых этого психолога и статистику по ним"""
    users = mongo_connect.db.users
    testees = users.find({'status':'testee', 'added_by':str(added_by), 'pre_del':None}, {'result':1, 'grade':1, '_id':0})
    if testees:
        return {testee['grade'] for testee in testees}
    return {}

def get_testees_by_grade(added_by: str, grade: str):
    """Принимает логин психолога, добавившего испытуемых, класс испытуемых.
    Возвращает список всех испытуемых этого психолога в заданном классе"""
    users = mongo_connect.db.users
    return users.find({'status':'testee', 'added_by':str(added_by), 'grade':str(grade), 'pre_del':None},
                {'result':1,'login':1, 'pas':1, 'grade':1, 'tests':1, 'create_date':1})

def get_user_by_login(login: str):
    """Принимает логин пользователшя, возвращает его данные в словаре, если такого пользователя нет
    или подошел срок удаления, функция возвращает None"""
    users = mongo_connect.db.users
    user_data = users.find_one({'login':str(login), '$or':[{'pre_del':None}, {'pre_del':{'$gt':now_stamp()}}]})
    return user_data

def get_user_by_id(users_id):
    """Принимает логин пользователшя, возвращает его данные в словаре, если такого пользователя нет
    или подошел срок удаления, функция возвращает None"""
    users = mongo_connect.db.users
    user_data = users.find_one({'_id':obj_id(users_id), '$or':[{'pre_del':None}, {'pre_del':{'$gt':now_stamp()}}]})
    return user_data


def update_psy(old_login: str, login: str, pas: str, ident: str, tests: list, count: int, pre_del):
    """Принимает логин редактируемого психолога, новый логин, новый пароль, новый список тестов, новое доступное кол-во испытуемых,
    новый идентификатор, новое значение предварительного удаления. Обновляет данные у данного психолога"""
    users = mongo_connect.db.users
    users.update_one({'login':str(old_login).capitalize()}, {'$set':{'login':str(login).capitalize(), 'pas':encrypt(str(pas)), 'tests':tests, 'count':int(count),
                                    'ident':str(ident), 'pre_del':pre_del}})
    if old_login != login:
        users.update_many({'added_by':str(old_login).capitalize()}, {'$set':{'added_by':str(login).capitalize()}})
