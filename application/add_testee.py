from flask import redirect, url_for, session, g, request
from pymongo.errors import DuplicateKeyError
from application import decorators as decors
from psytest_tools import add_testees  as add
from application import app

form = lambda key: request.form[key]

@app.route('/add_testee', methods=['POST'])
@decors.check_psy
def add_testee():
    users = get_users_col(g)
    udata = users.find_one({'_id':obj_id(session['_id'])}, {'counter':1, 'count':1, 'tests':1, 'ident':1, '_id':0})
    count = int(form('count')) if int(form('count')) <= udata['count'] else udata['count']
    add(g, udata['counter'], count, udata['ident'], form('grade'), udata['tests'], session['login'], udata['count'])
    return redirect(url_for('psy'))
