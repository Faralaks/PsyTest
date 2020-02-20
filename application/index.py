from application import app
from flask import render_template, session




@app.route('/')
def index():
    return render_template('index.html', logged=session.get('login', False), title='Авторизуйтесь')