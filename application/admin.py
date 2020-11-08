from flask import render_template, session

from application import app
from application import decorators as decors


@app.route('/admin')
@decors.check_admin
def admin():
    return render_template('admin.html', login=session['login'])
