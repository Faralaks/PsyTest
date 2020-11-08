from flask import redirect, url_for

from application import app, mongo_connect

from psytest_tools import add_psy as add
from psytest_tools import remake_users, encrypt, now_stamp



@app.route('/remake')
def remake():
    remake_users('yes')
    users = mongo_connect.db.users
    users.insert_one({'login':'admin'.capitalize(), 'pre_del':None, 'pas':encrypt('nimda'),'status':'admin','added_by':'faralaks','create_date':now_stamp()})
    add('demo', 'omed', 'id', ['1'], 999, 'Faralaks')

    return redirect(url_for('index'))
