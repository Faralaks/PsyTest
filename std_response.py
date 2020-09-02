from flask import jsonify


def success():
    return jsonify({'kind': 'Suc'})


def duplicate_key_err(err):
    field = list(err.details['keyValue'].keys())[0]
    return jsonify({'kind': 'DuplicatedField', 'field': field})


def unk_err():
    return jsonify({'kind': 'Fatal', 'msg': 'Произошла неизвестная ошибка, если проблема повториться, обратитесь к администратору!'})


