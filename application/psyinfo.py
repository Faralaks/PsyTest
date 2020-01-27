from application import app
from flask import render_template, redirect, url_for, session, g
from psytest_tools import *




@app.route('/psyinfo/<_id>', methods=['GET', 'POST'])
@app.route('/psyinfo/<_id>/<sort_by>', methods=['GET', 'POST'])
def psyinfo(_id, sort_by='result'):
    if check_session(g, 'admin', session):
        users = get_users_col(g)
        if request.method == 'GET':
            psy_data = get_psy_data(g, _id, ('login', 'pas', 'pre_del', 'ident', 'count', 'tests'))
            testees = get_testees(g, obj_id(_id)).sort(sort_by, 1)
            return  render_template('psyinfo.html', _id=_id, psy_data=psy_data, testees=testees, dec=decrypt, t2st=stamp2str, logged=True, login=session['login'])

        if request.method == 'POST':
            try:
                tests = [str(i) for i in range(1, 3) if  form_get('t'+str(i), None) != None]
                pre_del = now_stamp() + 259200 if form_get('del', None) == 'yes' else None
                update_psy(g, _id, form('login'), form('password'), tests, form('count'), form('ident'), pre_del)
            except DuplicateKeyError: return redirect(url_for(session.get('status', 'index'), msg='Такой Логин или Идентификатор уже существует'))
            #except: return redirect(url_for(session.get('status', 'index'), msg='Произошла неизвестная ошибка, если проблема не исчезнет, обратитесь к администратору!'))
            return redirect(url_for('admin'))
    else:
        return redirect(url_for('logout'))