from application import app
from flask import render_template, session, request, url_for, redirect, jsonify
from application import decorators as decors
from psytest_tools import b64dec, del_danger_res, del_clear_res, vprint
from std_response import err

form = lambda key: request.form[key]
form_get = lambda key, ret: request.form.get(key, ret)

del_res_type_decode = {'Не рискует': del_clear_res, 'Рискует': del_danger_res}

@app.route('/api/del_result', methods=['POST'])
@decors.check_psy
def del_result():
    prev_res = form_get('prevRes', None)
    login = form_get('testeeLogin', None)
    grade = form_get('grade', None)
    reason = form_get('reason', None)

    if del_res_type_decode.get(prev_res, None) is None: return err('Не был получен корректный предыдущий Результат испытуемого')
    if login is None: return err('Не был получен Логин Испытуемого')
    if grade is None: return err('Не был получен Класс испытуемого')
    if reason is None: return err('Не была получена Причина удаления испытуемого')

    try:
        del_res_type_decode[prev_res](login, session['login'], grade, reason)
        return jsonify(kind='Good')
    except:
        err('Возникла ошибка при удалении результата')