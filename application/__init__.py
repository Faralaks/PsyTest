from flask import Flask, url_for
app = Flask(__name__)
import application.add as add
import application.admin as admin
import application.index as index
import application.login as login
import application.logout as logout
import application.psy as psy
import application.psyinfo as psyinfo
import application.remake as remake
