from psytest_tools import get_user_by_login, get_grades_by_psy, b64enc, b64dec, vprint
from flask import render_template, redirect, url_for, session
from application import decorators as decors
from application import app




@app.route('/psy/')
@app.route('/psy/<sort_by>')
@decors.check_psy
def psy(sort_by='result'):
    user = get_user_by_login(session['login'])
    counters = {'whole':0, 'not_yet':0, 'clear':0, 'danger':0}
    for stats in user['grades'].values():
        counters['whole'] += stats.get('whole', 0)
        counters['not_yet'] += stats.get('not_yet', 0)
        counters['clear'] += stats.get('clear', 0)
        counters['danger'] += stats.get('danger', 0)
    return render_template('psy.html', logged=True, login=session['login'], status='psy', count=user['count'], grades=user['grades'],
                           counters=counters, b64enc=b64enc, b64dec=b64dec, cur_url=url_for('psy'), title='Психолог')