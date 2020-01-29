#!/usr/bin/python3
# -*- coding: utf8 -*-
from sys import platform
import sys
sys.path.insert(0, '/var/www/html/psytest')


def run(port: int):
    """Запускает flask-сервер согласно текущей платформе.
    Функция принимает ПОРТ, на котором будет работать сервер."""
    if platform != "darwin" and platform != "win32":
        app.run(host="127.0.0.1", port=port)
    else:
        app.run(port=port)
from application import app as application

if __name__ == '__main__':
    application.config.from_object('config')
    #run(81)
    
