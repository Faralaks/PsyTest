from flask import session, redirect, url_for, g, session
from bson.objectid import ObjectId as obj_id
from functools import wraps
from psytest_tools import *


def check_session(fn):
    """Проверяет, активна ли сессия и доступна ли ему эта страница."""
    @wraps(fn)
    def wrapper(*args, **kwargs): 
        ses = session
        try:
            col = get_users_col(g) 
            real_user = col.find_one({'_id':obj_id(ses['_id']),'$or':[{'pre_del':None}, {'pre_del':{'$gt':now_stamp()}}]},
                    {'_id':0,'status':1, 'login':1, 'pas':1})
            if real_user:
                if (now() < ses['timeout'] and
                        real_user['status'] == ses['status'] and
                        real_user['login'] == ses['login'] and
                        real_user['pas'] == ses['pas']):
                    return fn(*args, **kwargs)
            return redirect(url_for('logout'))
        except: 
            return redirect(url_for('logout'))
    return wrapper
