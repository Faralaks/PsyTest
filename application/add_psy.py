from flask import session, request, jsonify
from pymongo.errors import DuplicateKeyError
from application import decorators as decors
from std_response import duplicate_key_err, success, err as er
from psytest_tools import add_psy as add
from application import app

form = lambda key: request.form[key]
form_get = lambda key, ret: request.form.get(key, ret)


@app.route('/api/add_psy', methods=['POST'])
@decors.check_admin
def add_psy():
    try:
        tests = [str(i) for i in range(1, 3) if form_get('t' + str(i), None) is not None]
        add(form('login'), form('password'), form('ident'), tests, form('count'), session['login'])
    except DuplicateKeyError as err:
        return duplicate_key_err(err)
    except: return er("Неизвестная при попытке добавить психолога!")

    return success()