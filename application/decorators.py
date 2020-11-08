from functools import wraps

from flask import redirect, url_for, session

from psytest_tools import check_session


def check_admin(fn):
    """Проверяет, активна ли сессия и доступна ли зашедшему эта страница."""
    @wraps(fn)
    def wrapper(*args, **kwargs): 
        if check_session('admin', session):
            return fn(*args, **kwargs)
        return redirect(url_for('logout'))
    return wrapper

def check_psy(fn):
    """Проверяет, активна ли сессия и доступна зашедшему ему эта страница."""
    @wraps(fn)
    def wrapper(*args, **kwargs): 
        if check_session('psy', session):
            return fn(*args, **kwargs)
        return redirect(url_for('logout'))
    return wrapper

def check_testee(fn):
    """Проверяет, активна ли сессия и доступна ли зашедшему эта страница."""
    @wraps(fn)
    def wrapper(*args, **kwargs): 
        if check_session('testee', session):
            return fn(*args, **kwargs)
        return redirect(url_for('logout'))
    return wrapper

def check_admin_or_psy(fn):
    """Проверяет, активна ли сессия и доступна зашедшему ему эта страница."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('status') == 'admin':
            if check_session('admin', session):
                return fn(*args, **kwargs)
        else:
            if check_session('psy', session):
                return fn(*args, **kwargs)
        return redirect(url_for('logout'))
    return wrapper
