from flask import render_template, redirect, url_for, session, request
from psytest_tools import get_all_psys, gen_pass, decrypt, stamp2str
from application import decorators as decors
from application import app, mongo_connect 



@app.route('/admin')
@app.route('/admin/<sort_by>')
@decors.check_admin
def admin(sort_by='create_date'):
    users = mongo_connect.db.users
    psys = get_all_psys().sort(sort_by, 1)
    counters = {'psy_count':users.count_documents({'status':'psy'}),
                'testee_count':users.count_documents({'status':'testee'}),}
    return render_template('admin.html', msg=request.args.get('msg'), logged=True, login=session['login'], psys=psys, counters=counters, pas=gen_pass(12), dec=decrypt, t2st=stamp2str)
