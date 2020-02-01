from psytest_tools import get_user_by_login, get_grades_by_psy, b64enc, decrypt
from flask import render_template, redirect, url_for, session, request
from application import decorators as decors
from application import app, mongo_connect



@app.route('/psy_info/<login>/')
@app.route('/psy_info/<login>/<sort_by>')
@decors.check_admin
def psy_info(login, sort_by='create_date'):
    users = mongo_connect.db.users
    grades = get_grades_by_psy(login)
    counters = {'testee_count':users.count_documents({'status':'testee', 'added_by':session['login'], 'pre_del':None})}
    psy = get_user_by_login(login)
    return render_template('psy_info.html', msg=request.args.get('msg'), logged=True, login=session['login'], psy=psy, counters=counters, grades=grades,
                           back_url=url_for('admin'), dec=decrypt, b64enc=b64enc)
