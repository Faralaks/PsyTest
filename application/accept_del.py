from application import app
from flask import request
from application import  decorators as decors
from psytest_tools import get_user_by_login, accept_del as accept
from std_response import err, success

form = lambda key: request.form[key]
form_get = lambda key, ret: request.form.get(key, ret)



@app.route('/api/accept_del', methods=['POST'])
@decors.check_admin
def accept_del():
    login = form_get('testeeLogin', None)
    if login is None:
        return err('Не был получен Логин испытуемого')

    testee = get_user_by_login(login)
    accept(testee['login'], testee['added_by'], testee['grade'])
    return success()