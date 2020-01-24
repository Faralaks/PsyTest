from flask import Flask, g, redirect, render_template, request, url_for, session, escape, send_file
from pymongo.errors import DuplicateKeyError
from random import randint
from sys import platform
from pprint import pprint as pp
from psytest_tools import *

from time import time

app = Flask(__name__)
app.config.from_object('config')


insert = lambda col, **dock : col.insert_one(dock).inserted_id
update_user = lambda col, _id, **new : col.update_one({'_id':obj_id(_id)}, { "$set":new})

form = lambda key: request.form[key]
form_get = lambda key, ret: request.form.get(key, ret)

result_code = {'1': ['Любит печенье', 'Не любит печенье'],
            '2': ['Любит изюм', 'Не любит изюм']
            }


@app.route('/remake')
def remake():
    users = get_users_col(g)
    users.insert_one({'login':'Faralaks'.capitalize(), 'pre_del':None, 'pas':encrypt(''),'status':'admin','added_by':'faralaks','create_date':now_stamp()})
    users.insert_one({'login':'admin'.capitalize(), 'pre_del':None, 'pas':encrypt('admin'),'status':'admin','added_by':'faralaks','create_date':now_stamp()})
    remake_users(g, 'yes')
    
    return '<h1>REMAKED</h1>'

@app.route('/login', methods=['POST'])
def login():
    user_data = get_user(g, form('login').capitalize(), encrypt(form('password')))
    if user_data != False:
        session['_id'] = str(user_data['_id'])
        session['login'] = user_data['login']
        session['pas'] = user_data['pas']
        session['timeout'] = now() + dt.timedelta(days=1)
        session['status'] = user_data['status']
        return redirect(url_for(session['status']))
    return render_template('index.html', bad_auth=True)
    

@app.route('/logout')
def logout():
    for i in ('_id', 'login', 'pas', 'status', 'timeout'):
        try: del session[i]
        except: continue
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html', logged=session.get('login', False))

@app.route('/admin')
@app.route('/admin/<sort_by>')
def admin(sort_by='create_date'):
    if check_session(g, 'admin', session):
        users = get_users_col(g)
        psys = get_all_psys(g).sort(sort_by, 1)
        counters = {'psy_count':users.count_documents({'status':'psy'}),
                    'testee_count':users.count_documents({'status':'testee'}),}
        return render_template('admin.html', msg=request.args.get('msg'), logged=True, login=session['login'], psys=psys, counters=counters, pas=gen_pass(12), dec=decrypt, t2st=stamp2str)
    else:
        return redirect(url_for('logout'))


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



if platform == "win32": app.run(port=5000)#host='0.0.0.0')
else: app.run(debug=False, host='0.0.0.0', port=5001)
