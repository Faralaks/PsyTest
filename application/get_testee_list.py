from psytest_tools import b64enc, b64dec, get_testees_by_grade, get_user_by_login, decrypt, stamp2str, get_grades_by_psy
from application import app, mongo_connect
from application import decorators as decors
from flask import session, render_template, url_for, jsonify
from std_response import success, duplicate_key_err, unk_err

form = lambda key: request.form[key]
form_get = lambda key, ret: request.form.get(key, ret)


@app.route('/api/get_testee_list')
@decors.check_admin_or_psy
def get_testee_list():
    grade = form_get('grade', None)
    login = form_get('psyLogin', None)

    if grade is None: return unk_err('Не было получено название класса')
    if login is None: return unk_err('Не был получен логин психолога')

    return jsonify(testee_list=get_testees_by_grade(login, grade))
