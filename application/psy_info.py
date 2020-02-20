from psytest_tools import get_user_by_login, get_grades_by_psy, b64enc, decrypt, b64dec
from flask import render_template, redirect, url_for, session, request
from application import decorators as decors
from application import app



@app.route('/psy_info/<login>/')
@app.route('/psy_info/<login>/<sort_by>')
@decors.check_admin
def psy_info(login, sort_by='create_date'):
    psy = get_user_by_login(login)
    counters = {'whole':0, 'not_yet':0, 'clear':0, 'danger':0}
    for stats in psy['grades'].values():
        counters['whole'] += stats.get('whole', 0)
        counters['not_yet'] += stats.get('not_yet', 0)
        counters['clear'] += stats.get('clear', 0)
        counters['danger'] += stats.get('danger', 0)
    session['psy_login'] = login
    return render_template('psy_info.html', msg=request.args.get('msg'), logged=True, login=session['login'], psy=psy, counters=counters, grades=psy['grades'],
                           back_url=url_for('admin'), dec=decrypt, b64enc=b64enc, b64dec=b64dec, title=psy['login']+' | Информация')
