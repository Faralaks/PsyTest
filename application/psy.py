from psytest_tools import get_user_by_login, get_grades_by_psy, b64enc, b64dec
from flask import render_template, redirect, url_for, session
from application import decorators as decors
from application import app




@app.route('/psy')
@decors.check_psy
def psy():
    return render_template('psy.html', login=session['login'])