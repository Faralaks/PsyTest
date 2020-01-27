from flask import Flask, url_for
from flask_pymongo import PyMongo
from config import MONGO_URI

app = Flask(__name__)
mongo_connect = PyMongo(app, MONGO_URI)

import application.add_psy as add_psy
import application.add_testee as add_testee
import application.admin as admin
import application.decorators as decorators
import application.index as index
import application.login as login
import application.logout as logout
import application.psy as psy
import application.psyinfo as psyinfo
import application.remake as remake
