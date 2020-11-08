from flask import redirect, url_for, session

from application import app


@app.route('/logout')
def logout():
    for i in ('_id', 'login', 'pas', 'status', 'timeout'):
        try: del session[i]
        except: continue
    return redirect(url_for('index'))