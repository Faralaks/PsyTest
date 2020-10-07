from flask import jsonify


def success():
    return jsonify({'kind': 'Suc'})


def duplicate_key_err(err):
    field = list(err.details['keyValue'].keys())[0]
    return jsonify({'kind': 'DuplicatedField', 'field': field})


def err(msg=None):
    if msg: return jsonify(kind='Fatal', msg=msg)
    return jsonify(msg='Произошла неизвестная ошибка, если проблема повториться, обратитесь к администратору!')

def err_in_html(msg=None):
    if msg: return '<h1>%s</h1>'%msg
    return '<h1>Проищошла неизвестная ошибка на стороне сервера</h1>'


