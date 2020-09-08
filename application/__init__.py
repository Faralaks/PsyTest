from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object('config')
mongo_connect = PyMongo(app)

import application.add_psy as add_psy
import application.add_testee as add_testee
import application.admin as admin
import application.decorators as decorators
import application.del_result as del_result
import application.download as download
import application.edit_psy as edit_psy
import application.grade as grade
import application.index as index
import application.login as login
import application.logout as logout
import application.messages as messages
import application.psy as psy
import application.get_grade_list as get_grade_list
import application.get_testee_list as get_testee_list
import application.remake as remake
import application.testee as testee
