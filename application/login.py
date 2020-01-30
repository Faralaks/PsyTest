from flask import render_template, redirect, url_for, session, request
from application import app
from psytest_tools import *

form = lambda key: request.form[key]


@app.route('/login', methods=['POST'])
def login():
    user_data = get_user(form('login').capitalize())
    if user_data:
        vprint()
        if user_data['pas'] == encrypt(form('password')):
            session['_id'] = str(user_data['_id'])
            session['login'] = user_data['login']
            session['pas'] = user_data['pas']
            session['timeout'] = now() + dt.timedelta(days=1)
            session['status'] = user_data['status']
            return redirect(url_for(session['status']))
    return render_template('index.html', bad_auth=True)