from flask import render_template, session
from application import decorators as decors
from application import app
from flask import render_template, session

from application import app
from application import decorators as decors


@app.route('/psy')
@decors.check_psy
def psy():
    return render_template('psy.html', login=session['login'])