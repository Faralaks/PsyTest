from flask import redirect, url_for, session, request, jsonify
from pymongo.errors import DuplicateKeyError
from application import decorators as decors
from std_response import duplicate_key_err, success, unk_err
from psytest_tools import add_psy as add
from application import app
from psytest_tools import vprint

form = lambda key: request.form[key]


@app.route('/api/add_psy', methods=['POST'])
@decors.check_admin
def add_psy():
    try:
        tests = [str(i) for i in range(1, 3) if form_get('t' + str(i), None) is not None]
        add(form('login'), form('password'), form('ident'), tests, form('count'), session['login'])
    except DuplicateKeyError as err:
        return duplicate_key_err(err)
    except: return unk_err()

    return success()