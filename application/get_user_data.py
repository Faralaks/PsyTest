from flask import session, request

from application import app
from psytest_tools import get_user_by_login, fixed_jsonify
from std_response import err

form = lambda key: request.form[key]
form_get = lambda key, ret: request.form.get(key, ret)

@app.route('/api/get_user_data', methods=['POST'])
def get_user_data():
    login = form('login') if form_get('login', None) and session.get('status') == 'admin' else session.get('login', None)
    if login is None:
        return err('Не был получен Логин пользователя')
    return fixed_jsonify(kind='Good', userData=get_user_by_login(login))
