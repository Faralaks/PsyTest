from flask import redirect, url_for, session, request, jsonify
from pymongo.errors import DuplicateKeyError
from application import decorators as decors
from psytest_tools import update_psy as update, now_stamp, vprint, get_user_by_login, fixed_jsonify
from application import app
from std_response import success, duplicate_key_err, unk_err

form = lambda key: request.form[key]
form_get = lambda key, ret: request.form.get(key, ret)

@app.route('/api/get_user_data', methods=['POST'])
def get_user_data():
    login = form('login') if form_get('login', None) and session.get('status') == 'admin' else session.get('login', None)
    if login is None:
        return unk_err('Не был получен Логин пользователя')
    vprint(login)
    return fixed_jsonify(kind='Good', userData=get_user_by_login(login))
