from flask import redirect, url_for, session, request, jsonify
from pymongo.errors import DuplicateKeyError
from application import decorators as decors
from psytest_tools import update_psy as update, now_stamp, vprint
from application import app
from std_response import success, duplicate_key_err, unk_err

form = lambda key: request.form[key]
form_get = lambda key, ret: request.form.get(key, ret)

err_decode = {'ident':'Идентификатор', 'login':'Логин'}

@app.route('/edit_psy/<login>', methods=['POST'])
@decors.check_admin
def edit_psy(login):
    try:
        tests = [str(i) for i in range(1, 3) if form_get('t' + str(i), None) is not None]
        pre_del = now_stamp() + 259200 if form_get('del', None) == 'Yes' else None
        update(login, form('login'), form('password'), form('ident'), tests, form('count'), pre_del)
    except DuplicateKeyError as err:
        return duplicate_key_err(err)
    except: return unk_err("Неизвестная при попытке редактирования данных психолога!")

    return success()