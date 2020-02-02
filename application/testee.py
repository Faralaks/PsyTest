from application import decorators as decors
from psytest_tools import get_user_by_login, set_test_index
from flask import render_template, session, request
from application import app



@app.route('/testee', methods=['GET', 'POST'])
@decors.check_testee
def testee():
    user = get_user_by_login(session['login'])
    try:
        if request.method == 'POST':
            nxt = user['step']
            set_test_index(session['login'], nxt + 1)
            return render_template('test_%s.html' % user['tests'][nxt], login=session['login'])

        elif request.method == 'GET':
            if user['step'] == 'start':
                nxt = 0
                set_test_index(session['login'], nxt + 1)
            return render_template('test_%s.html'%user['step'], logged=True, login=session['login'])
    except IndexError:
        return render_template('test_stop.html', login=session['login'])