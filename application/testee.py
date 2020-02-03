from application import decorators as decors
from psytest_tools import get_user_by_login, set_test_index, set_result, inc_grade_clear, inc_grade_danger
from flask import render_template, session, request, redirect, url_for
from application import app

form = lambda key: request.form[key]

@app.route('/testee', methods=['GET', 'POST'])
@decors.check_testee
def testee():
    user = get_user_by_login(session['login'])
    try:
        if request.method == 'POST':
            try:
                res = int(form('q1'))
            except KeyError:
                return render_template('test_%s.html' % user['tests'][user['step']], login=session['login'], msg="Вы пропустили этот вопрос!")

            new_res = 'Нет результата'
            if res == 0:
                new_res = 'Рискует'
                inc_grade_danger(user['added_by'], user['grade'])
            elif  res == 1:
                inc_grade_clear(user['added_by'], user['grade'])
                new_res = 'Не рискует'

            set_result(session['login'], new_res)
            set_test_index(session['login'], user['step'] + 1)
            return redirect(url_for('testee'))

        elif request.method == 'GET':
            nxt = user['step']
            if user['step'] == 'start':
                set_test_index(session['login'], 0)
                return render_template('test_start.html', login=session['login'])
            return render_template('test_%s.html'%user['tests'][nxt], login=session['login'])
    except IndexError:
        return render_template('test_stop.html', login=session['login'])