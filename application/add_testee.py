from psytest_tools import  get_user_by_login, b64dec
from flask import redirect, url_for, session, request
from psytest_tools import add_testees  as add
from application import decorators as decors
from application import app

from  pprint import pprint as pp

form = lambda key: request.form[key]


@app.route('/add_testee', methods=['POST'])
@app.route('/add_testee/<ret>', methods=['POST'])
@decors.check_psy
def add_testee(ret=None):
    psy = get_user_by_login(session['login'])
    count = int(form('count')) if int(form('count')) <= psy['count'] else psy['count']
    add(psy['counter'], count, psy['ident'], form('grade'), psy['tests'], session['login'], psy['count'])
    if ret: return redirect(b64dec(ret))
    return redirect(url_for('psy'))
