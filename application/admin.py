from flask import render_template, redirect, url_for, session, request
from psytest_tools import get_all_psys, gen_pass, decrypt, stamp2str, vprint
from application import decorators as decors
from application import app



@app.route('/admin')
@app.route('/admin/<sort_by>')
@decors.check_admin
def admin(sort_by='create_date'):
    psys = get_all_psys().sort(sort_by, 1)
    big_counters = {'psys':0, 'whole':0, 'not_yet':0, 'clear':0, 'danger':0}
    psy_and_stats = []

    for psy in psys:
        big_counters['psys'] += 1
        psy_and_stats.append({'login':psy['login'], 'pas':psy['pas'] ,'create_date':psy['create_date'], 'pre_del':psy.get('pre_del'), 'ident':psy['ident'], 'tests':psy['tests'],
                             'count':psy['count'], 'counters':{'whole':0, 'not_yet':0, 'clear':0, 'danger':0}})

        for stats in psy['grades'].values():
            big_counters['whole'] += stats.get('whole', 0)
            psy_and_stats[-1]['counters']['whole'] += stats.get('whole', 0)
            big_counters['not_yet'] += stats.get('not_yet', 0)
            psy_and_stats[-1]['counters']['not_yet'] += stats.get('not_yet', 0)
            big_counters['clear'] += stats.get('clear', 0)
            psy_and_stats[-1]['counters']['clear'] += stats.get('clear', 0)
            big_counters['danger'] += stats.get('danger', 0)
            psy_and_stats[-1]['counters']['danger'] += stats.get('danger', 0)
        vprint(psy_and_stats)
    return render_template('admin.html', msg=request.args.get('msg'), logged=True, login=session['login'], psys=psy_and_stats, counters=big_counters, pas=gen_pass(12), dec=decrypt, t2st=stamp2str)
