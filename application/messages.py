from application import app
from flask import render_template, session, escape, url_for, request, redirect
from application import  decorators as decors
from psytest_tools import get_user_by_login, b64dec, b64enc, accept_del


@app.route('/messages/<login>', methods=['GET', 'POST'])
@decors.check_admin
def messages(login):
    testee = get_user_by_login(login)
    enc_name = b64enc(testee['grade'])
    if request.method == 'GET':
        return render_template('messages.html', logged=session.get('login', False), title='Сообщение об удалении', testee_login=testee['login'],
                               name=(enc_name, testee['grade']), psy_login=session['psy_login'], msg=escape(b64dec(testee['msg'])),
                               back_url=url_for('grade', name=enc_name))
    elif request.method == 'POST':
        accept_del(testee['login'], testee['added_by'], testee['grade'])
        return redirect(url_for('grade', name=enc_name))