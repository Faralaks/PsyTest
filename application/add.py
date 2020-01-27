from application import app
from flask import redirect, url_for, session, g
from psytest_tools import *
#from application import decorators as decors



@app.route('/add/<status>', methods=['POST'])
def add(status):
    if check_session(g, 'admin', session) and status == 'psy':
        try:
            tests = [str(i) for i in range(1, 3) if form_get('t'+str(i), None) != None]
            add_psy(g, form('login'), form('password'), form('ident'), tests, form('count'), session['_id'])
        except DuplicateKeyError: return redirect(url_for(session.get('status', 'index'), msg='Такой Логин или Идентификатор уже существует'))
        #except: return redirect(url_for(session.get('status', 'index'), msg='Произошла неизвестная ошибка, если проблема не исчезнет, обратитесь к администратору!'))
    
    elif check_session(g, 'psy', session) and status == 'testee':
        users = get_users_col(g)
        udata = users.find_one({'_id':obj_id(session['_id'])}, {'counter':1, 'count':1, 'tests':1, 'ident':1, '_id':0})
        count = int(form('count')) if int(form('count')) <= udata['count'] else udata['count']
        add_testees(g, udata['counter'], count, udata['ident'], form('grade'), udata['tests'], session['_id'], udata['count'])
    return redirect(url_for(session.get('status', 'index')))