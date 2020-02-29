from application import app
from flask import render_template, session, request, url_for, redirect
from application import decorators as decors
from psytest_tools import b64dec, del_danger_res, del_clear_res


@app.route('/del_result/<grade>/<login>/<prev_res>', methods=['GET', 'POST'])
@decors.check_psy
def del_result(grade, login, prev_res):
    if request.method == 'GET':
        return render_template('del_result.html', logged=session.get('login', False), login=session['login'], name=(grade, b64dec(grade)),
                               testee_login=login, back_url=url_for('grade', name=grade), prev_res=prev_res, title='Удаление результата')
    elif request.method == 'POST':
        if prev_res == 'clear':
            del_clear_res(login, session['login'], b64dec(grade), request.form['reason'])
        elif prev_res == 'danger':
            del_danger_res(login, session['login'], b64dec(grade), request.form['reason'])
        else: return '<h1>Ошибка при изменении статистики. Не верный параметр адресной строки</h1>'
        return redirect(url_for('grade', name=grade))
    return redirect(url_for('grade', name=grade))
