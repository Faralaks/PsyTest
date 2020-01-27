from application import app
from flask import Blueprint, render_template, redirect, url_for, session
from psytest_tools import *




@app.route('/logout')
def logout():
    for i in ('_id', 'login', 'pas', 'status', 'timeout'):
        try: del session[i]
        except: continue
    return redirect(url_for('index'))