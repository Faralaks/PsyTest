#!/usr/bin/python3
# -*- coding: utf8 -*-
from sys import platform, path
path.insert(0,  '/home/git/psytest')

from application import app as application
application.config.from_object('config')
