from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object('config')
mongo_connect = PyMongo(app)

import application.add_psy as add_psy
import application.add_testee as add_testee
import application.admin as admin
import application.decorators as decorators
import application.grade as grade
import application.index as index
import application.login as login
import application.logout as logout
import application.psy as psy
import application.psyinfo as psyinfo
import application.remake as remake
