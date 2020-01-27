from application import app
from flask import render_template, redirect, url_for, session, g
from psytest_tools import *



@app.route('/psy')
@app.route('/psy/<sort_by>')
def psy(sort_by='result'):
    if check_session(g, 'psy', session):
        users = get_users_col(g)
        cur_count = get_psy_data(g, session['_id'], ('count',))['count']
        testees = get_testees(g, session['_id']).sort(sort_by, 1)
        counters = {'testee_count':users.count_documents({'status':'testee', 'created_by':session['_id'], 'pre_del':None})}
        return render_template('psy.html', logged=True, login=session['login'], count=cur_count, testees=testees, counters=counters, dec=decrypt, t2st=stamp2str)
    else:
        return redirect(url_for('logout'))