from psytest_tools import b64enc, b64dec, get_testees_by_grade, get_user_by_login, decrypt, stamp2str, get_grades_by_psy, vprint
from application import app, mongo_connect
from application import decorators as decors
from flask import session, render_template, url_for




@app.route('/grade/<name>/')
@app.route('/grade/<name>/<sort_by>')
@decors.check_admin_or_psy
def grade(name, sort_by='result'):
    dec_name = b64dec(name)
    
    psy_login = session['login']
    back_url = url_for('psy')
    if session['status'] == 'admin':
        psy_login= session['psy_login']
        back_url = url_for('psy_info', login=session['psy_login'])

    counters = get_grades_by_psy(psy_login)['grades'][name]
    cur_count = get_user_by_login(psy_login)['count']
    testees = get_testees_by_grade(psy_login, dec_name).sort(sort_by, 1)

    return render_template('grade.html', logged=True, login=psy_login, count=cur_count, testees=testees, counters=counters, name=(name, dec_name),
                            status=session['status'], back_url=back_url, dec=decrypt, t2st=stamp2str, b64enc=b64enc,
                           cur_url=url_for('grade', name=name), title=dec_name+' класс')
