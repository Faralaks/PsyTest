from flask import request, jsonify

from application import app
from application import decorators as decors
from psytest_tools import get_user_by_login
from std_response import err

form = lambda key: request.form[key]
form_get = lambda key, ret: request.form.get(key, ret)

@app.route('/api/get_grade_list', methods=['POST'])
@decors.check_admin
def get_grade_list():
    if form_get('psyLogin', None) is None:
        return err('Не был получен Логин психолога')

    return jsonify(kind='Good', gradeList=get_user_by_login(form('psyLogin')).get('grades', {}))
