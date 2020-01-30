from flask import redirect, url_for, session, request
from pymongo.errors import DuplicateKeyError
from application import decorators as decors
from psytest_tools import add_testees  as add
from psytest_tools import  get_user_by_login
from application import app

from  pprint import pprint as pp

form = lambda key: request.form[key]

@app.route('/add_testee', methods=['POST'])
@decors.check_psy
def add_testee():
    psy = get_user_by_login(session['login'])
    count = int(form('count')) if int(form('count')) <= psy['count'] else psy['count']
    add(psy['counter'], count, psy['ident'], form('grade'), psy['tests'], session['login'], psy['count'])
    return redirect(url_for('psy'))
