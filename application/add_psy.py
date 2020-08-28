from flask import redirect, url_for, session, request, jsonify
from pymongo.errors import DuplicateKeyError
from application import decorators as decors
from psytest_tools import add_psy as add
from application import app
from psytest_tools import vprint

form = lambda key: request.form[key]
form_get = lambda key, ret: request.form.get(key, ret)

err_decode = {'ident':'Идентификатор', 'login':'Логин'}

@app.route('/add_psy', methods=['POST'])
@decors.check_admin
def add_psy():
    try:
        tests = [str(i) for i in range(1, 3) if form_get('t' + str(i), None) is not None]
        add(form('login'), form('password'), form('ident'), tests, form('count'), session['login'])
    except DuplicateKeyError as err:
        field = list(err.details['keyValue'].keys())[0]
        return jsonify({'kind':'DuplicatedField', 'field':field})
    #except: return jsonify({'kind':'Fatal', 'msg':'Произошла неизвестная ошибка, если проблема повториться, обратитесь к администратору!'})
    return jsonify({'kind':'Suc'})