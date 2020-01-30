from application import app
from psytest_tools import  b64dec




@app.route('/grade/<psy>/<name>')
def grade(psy, name):
    return '<h1>'+b64dec(psy)+b64dec(name)+'</h1>'