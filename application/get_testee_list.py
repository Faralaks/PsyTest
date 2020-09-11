import time

from psytest_tools import get_testees_by_grade, get_user_by_login, decrypt, stamp2str, get_grades_by_psy, vprint, fixed_jsonify
from application import app
from application import decorators as decors
from flask import session,  request
from std_response import success, duplicate_key_err, err

form = lambda key: request.form[key]
form_get = lambda key, ret: request.form.get(key, ret)


@app.route('/api/get_testee_list', methods=['POST'])
@decors.check_admin_or_psy
def get_testee_list():
    grade = form_get('grade', None)
    login = form_get('psyLogin', None) if session['status'] == 'admin' else session['login']

    if grade is None: return err('Не было получено название класса')
    if login is None: return err('Не был получен логин психолога')

    return fixed_jsonify(kind='Good', testeeList=list(get_testees_by_grade(login, grade)))
