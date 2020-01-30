from psytest_tools import get_user_by_login, get_grades_by_psy, decrypt, stamp2str, b64enc
from flask import render_template, redirect, url_for, session
from application import decorators as decors
from application import app, mongo_connect




@app.route('/psy')
@app.route('/psy/<sort_by>')
@decors.check_psy
def psy(sort_by='result'):
    users = mongo_connect.db.users
    cur_count = get_user_by_login(session['login'])['count']
    grades = get_grades_by_psy(session['login'])
    counters = {'testee_count':users.count_documents({'status':'testee', 'created_by':session['_id'], 'pre_del':None})}

    return render_template('psy.html', logged=True, login=session['login'], count=cur_count, grades=grades, counters=counters,
                           dec=decrypt, t2st=stamp2str, b64enc=b64enc)