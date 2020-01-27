from application import app
from flask import render_template, redirect, url_for, session, g, request
from psytest_tools import *



@app.route('/admin')
@app.route('/admin/<sort_by>')
def admin(sort_by='create_date'):
    if check_session(g, 'admin', session):
        users = get_users_col(g)
        psys = get_all_psys(g).sort(sort_by, 1)
        counters = {'psy_count':users.count_documents({'status':'psy'}),
                    'testee_count':users.count_documents({'status':'testee'}),}
        return render_template('admin.html', msg=request.args.get('msg'), logged=True, login=session['login'], psys=psys, counters=counters, pas=gen_pass(12), dec=decrypt, t2st=stamp2str)
    else:
        return redirect(url_for('logout'))