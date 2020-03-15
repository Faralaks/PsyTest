from psytest_tools import b64dec, decrypt, get_testees_by_grade_not_yet, make_filename, get_testees_by_grade_done, stamp2str
from application import app
from application import decorators as decors
from flask import session, render_template, url_for, redirect, send_file
from os import path
from openpyxl import Workbook
import docx




@app.route('/download/<name>/<target>')
@decors.check_admin_or_psy
def download(name, target):
    dec_name = b64dec(name)
    psy_login = session['login']
    if session['status'] == 'admin': psy_login= session['psy_login']

    if target == 'not_yet':
        testees = tuple(get_testees_by_grade_not_yet(psy_login, dec_name))
        doc = docx.Document()
        table = doc.add_table(rows=len(testees), cols=3)
        table.style = 'Table Grid'
        for row, testee in enumerate(testees):
            table.cell(row, 0).text = testee['login']
            table.cell(row, 1).text = decrypt(testee['pas'])
            table.cell(row, 2).text = '\n\n'
        filename = path.join(app.config['DOCKS_FOLDER'], make_filename(psy_login, 'docx'))
        doc.save(filename)
        return send_file(filename, cache_timeout=0, as_attachment=True)

    if target == 'done':
        testees = tuple(get_testees_by_grade_done(psy_login, dec_name))
        wb = Workbook()
        ws = wb.active
        ws.append(['Результат', 'Логин', 'Класс', 'Пройденные тесты', 'Дата создания'])
        for testee in testees:
            ws.append([testee['result'], testee['login'], testee['grade'], ' '.join(testee['tests']), stamp2str(testee['create_date'])])
        filename = path.join(app.config['DOCKS_FOLDER'], make_filename(psy_login, 'xlsx'))
        wb.save(filename)
        wb.close()
        return send_file(filename, cache_timeout=0, as_attachment=True)
