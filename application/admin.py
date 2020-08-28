from flask import render_template, redirect, url_for, session, request, jsonify
from psytest_tools import get_all_psys, gen_pass, decrypt, stamp2str
from application import decorators as decors
from application import app



@app.route('/admin', methods=['GET', 'POST'])
@decors.check_admin
def admin():
    if request.method == 'GET':
        return render_template('admin.html', login=session['login'],  title='Администратор | Главная страница')

    elif request.method == 'POST':
        psys = get_all_psys()
        big_counters = {'psy_count':0, 'whole':0, 'not_yet':0, 'clear':0, 'danger':0, 'msg':0}
        psy_and_stats = []

        for psy in psys:
            big_counters['psy_count'] += 1
            psy_and_stats.append({'login':psy['login'], 'pas':decrypt(psy['pas']) ,'create_date':stamp2str(psy['create_date']), 'pre_del':psy.get('pre_del'), 'ident':psy['ident'], 'tests':psy['tests'],
                                 'count':psy['count'], 'counters':{'whole':0, 'not_yet':0, 'clear':0, 'danger':0, 'msg':0}})

            for stats in psy['grades'].values():
                big_counters['whole'] += stats.get('whole', 0)
                psy_and_stats[-1]['counters']['whole'] += stats.get('whole', 0)
                big_counters['not_yet'] += stats.get('not_yet', 0)
                psy_and_stats[-1]['counters']['not_yet'] += stats.get('not_yet', 0)
                big_counters['clear'] += stats.get('clear', 0)
                psy_and_stats[-1]['counters']['clear'] += stats.get('clear', 0)
                big_counters['danger'] += stats.get('danger', 0)
                psy_and_stats[-1]['counters']['danger'] += stats.get('danger', 0)
                big_counters['msg'] += stats.get('msg', 0)
                psy_and_stats[-1]['counters']['msg'] += stats.get('msg', 0)
        return jsonify({'psys':psy_and_stats, 'stats':big_counters})

