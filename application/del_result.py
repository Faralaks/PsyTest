from application import app
from flask import render_template, session, request, url_for
from application import decorators as decors
from psytest_tools import b64dec


@app.route('/del_result/<grade>/<login>', methods=['GET', 'POST'])
@decors.check_psy
def del_result(grade, login):
    if request.method == 'GET':
        return render_template('del_result.html', logged=session.get('login', False), login=session['login'], grade=b64dec(grade), testee_login=login, back_url=url_for('grade', name=grade))
    elif request.method == 'POST':
        return '<h1>Удалено</h1>'
