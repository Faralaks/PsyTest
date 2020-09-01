from flask import render_template, redirect, url_for, session, request, jsonify
from psytest_tools import get_all_psys, gen_pass, decrypt, stamp2str, fixed_jsonify
from application import decorators as decors
from application import app



@app.route('/admin')
@decors.check_admin
def admin():
    return render_template('admin.html', login=session['login'],  title='Администратор | Главная страница')


@app.route('/api/get_psy_list', methods=['POST'])
@decors.check_admin
def get_psy_list():
        return fixed_jsonify(list(get_all_psys()))

