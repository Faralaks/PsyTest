from psytest_tools import b64enc, b64dec, get_testees_by_grade, get_user_by_login, decrypt, stamp2str, get_grades_by_psy, vprint, get_testees_by_grade_not_yet, now_str
from application import app, mongo_connect
from application import decorators as decors
from flask import session, render_template, url_for, redirect, send_file
from os import path
import docx




@app.route('/download/<name>/<target>')
@decors.check_admin_or_psy
def download(name, target):
    dec_name = b64dec(name)

    if target == 'not_yet':
        testees = tuple(get_testees_by_grade_not_yet(session['login'], dec_name))
        doc = docx.Document()
        table = doc.add_table(rows=len(testees), cols=3)
        table.style = 'Table Grid'
        for row, testee in enumerate(testees):
            table.cell(row, 0).text = testee['login']
            table.cell(row, 1).text = decrypt(testee['pas'])
            table.cell(row, 2).text = '\n\n'

        filename = path.join(app.config['DOCKS_FOLDER'], session['login']+'_'+now_str().replace(':', '_')+'.docx')
        doc.save(filename)
        return send_file(filename)

    else:
        return redirect(url_for(session['status']))
