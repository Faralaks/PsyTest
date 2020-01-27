from application import app
from flask import render_template, redirect, url_for, g
from psytest_tools import *



@app.route('/remake')
def remake():
    remake_users(g, 'yes')
    users = get_users_col(g)
    users.insert_one({'login':'Faralaks'.capitalize(), 'pre_del':None, 'pas':encrypt(''),'status':'admin','added_by':'faralaks','create_date':now_stamp()})
    users.insert_one({'login':'admin'.capitalize(), 'pre_del':None, 'pas':encrypt('admin'),'status':'admin','added_by':'faralaks','create_date':now_stamp()})
    
    return redirect(url_for('index'))