from flask import render_template, redirect, url_for, session, request
from psytest_tools import get_user_by_login
from application import decorators as decors
from application import app, mongo_connect 



@app.route('/testee')
@decors.check_testee
def testee():
    user = get_user_by_login(session['login'])
    return render_template('test_%s.html'%user['step'], logged=True, login=session['login'])