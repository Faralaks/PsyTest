from flask import redirect, url_for, session, request
from pymongo.errors import DuplicateKeyError
from application import decorators as decors
from psytest_tools import update_psy as update, now_stamp
from application import app

form = lambda key: request.form[key]
form_get = lambda key, ret: request.form.get(key, ret)

@app.route('/edit_psy/<login>', methods=['POST'])
@decors.check_admin
def edit_psy(login):
    if True:#try:
        tests = [str(i) for i in range(1, 3) if form_get('t' + str(i), None) is not None]
        pre_del = now_stamp() + 259200 if form_get('del', None) == 'Yes' else None
        update(login, form('login'), form('password'), form('ident'), tests, form('count'), pre_del)
    #except DuplicateKeyError: return redirect(url_for('psy_info', login=login, msg='Такой Логин или Идентификатор уже существует'))
    #except: return redirect(url_for('psy_info', login=login, msg='Произошла неизвестная ошибка, если проблема не исчезнет, обратитесь к администратору!'))
    return redirect(url_for('psy_info', login=form('login').capitalize()))