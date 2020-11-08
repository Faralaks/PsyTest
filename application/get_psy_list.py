from application import decorators as decors, app
from psytest_tools import get_all_psys, fixed_jsonify


@app.route('/api/get_psy_list', methods=['POST'])
@decors.check_admin
def get_psy_list():
        return fixed_jsonify(kind='Good', psyList=list(get_all_psys()))

