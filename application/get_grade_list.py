from psytest_tools import get_user_by_login, get_grades_by_psy, b64enc, decrypt, b64dec
from flask import render_template, redirect, url_for, session, request, jsonify
from application import decorators as decors
from application import app



@app.route('/get_grade_list/<login>', methods=['POST'])
@decors.check_admin
def get_grade_list(login):
    psy = get_user_by_login(login)
    counters = {'whole':0, 'not_yet':0, 'clear':0, 'danger':0, 'msg':0}
    for stats in psy.get('grades', {}).values():
        counters['whole'] += stats.get('whole', 0)
        counters['not_yet'] += stats.get('not_yet', 0)
        counters['clear'] += stats.get('clear', 0)
        counters['danger'] += stats.get('danger', 0)
        counters['msg'] += stats.get('msg', 0)
    session['psy_login'] = login
    return jsonify({'stats':counters, 'grades':list(psy['grades'].items())})
