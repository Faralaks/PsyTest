from flask import render_template, redirect, url_for
from application import app, mongo_connect
from psytest_tools import remake_users, encrypt, now_stamp
from psytest_tools import add_psy as add



@app.route('/remake')
def remake():
    remake_users('yes')
    users = mongo_connect.db.users
    users.insert_one({'login':'admin'.capitalize(), 'pre_del':None, 'pas':encrypt('nimda'),'status':'admin','added_by':'faralaks','create_date':now_stamp()})
    add('psy', 's', 'id', ['1'], 999, 'admin')

    return redirect(url_for('index'))
