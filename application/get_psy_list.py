from flask import render_template, redirect, url_for, session, request, jsonify
from psytest_tools import get_all_psys, gen_pass, decrypt, stamp2str, fixed_jsonify
from application import decorators as decors
from application import app



@app.route('/api/get_psy_list', methods=['POST'])
@decors.check_admin
def get_psy_list():
        return fixed_jsonify(kind='Good', psyList=list(get_all_psys()))

