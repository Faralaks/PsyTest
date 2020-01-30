from flask import session, redirect, url_for, g, session
from bson.objectid import ObjectId as obj_id
from functools import wraps
from psytest_tools import check_session



def check_admin(fn):
    """Проверяет, активна ли сессия и доступна ли ему эта страница."""
    @wraps(fn)
    def wrapper(*args, **kwargs): 
        if check_session('admin', session):
            return fn(*args, **kwargs)
        return redirect(url_for('logout'))
    return wrapper

def check_psy(fn):
    """Проверяет, активна ли сессия и доступна ли ему эта страница."""
    @wraps(fn)
    def wrapper(*args, **kwargs): 
        if check_session('psy', session):
            return fn(*args, **kwargs)
        return redirect(url_for('logout'))
    return wrapper

def check_testee(fn):
    """Проверяет, активна ли сессия и доступна ли ему эта страница."""
    @wraps(fn)
    def wrapper(*args, **kwargs): 
        if check_session('testee', session):
            return fn(*args, **kwargs)
        return redirect(url_for('logout'))
    return wrapper