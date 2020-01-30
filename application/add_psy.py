from flask import redirect, url_for, session, request
from pymongo.errors import DuplicateKeyError
from application import decorators as decors
from psytest_tools import add_psy as add
from application import app

form = lambda key: request.form[key]
form_get = lambda key, ret: request.form.get(key, ret)

@app.route('/add_psy', methods=['POST'])
@decors.check_admin
def add_psy():
    try:
        tests = [str(i) for i in range(1, 3) if form_get('t' + str(i), None) is not None]
        add(form('login'), form('password'), form('ident'), tests, form('count'), session['login'])
    except DuplicateKeyError: return redirect(url_for(session.get('status', 'index'), msg='Такой Логин или Идентификатор уже существует'))
    #except: return redirect(url_for(session.get('status', 'index'), msg='Произошла неизвестная ошибка, если проблема не исчезнет, обратитесь к администратору!'))
    return redirect(url_for('admin'))