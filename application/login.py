from application import app
from flask import render_template, redirect, url_for, session, g, request
from psytest_tools import *

form = lambda key: request.form[key]
#form_get = lambda key, ret: request.form.get(key, ret)


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