from psytest_tools import get_user_by_login, get_grades_by_psy, b64enc, decrypt, b64dec, vprint
from flask import render_template, redirect, url_for, session, request, jsonify
from application import decorators as decors
from application import app
from std_response import unk_err

form = lambda key: request.form[key]
form_get = lambda key, ret: request.form.get(key, ret)

@app.route('/api/get_grade_list', methods=['POST'])
@decors.check_admin
def get_grade_list():
    if form_get('psyLogin', None) is None:
        return unk_err('Не был получен Логин психолога')

    return jsonify(kind='Good', gradeList=list(get_user_by_login(form('psyLogin')).get('grades', {}).items()))
