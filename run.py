#!/usr/bin/python3
from flask import g 
from sys import platform
from psytest_tools import *

from time import time



def run(port: int):
    """Запускает flask-сервер согласно текущей платформе.
    Функция принимает ПОРТ, на котором будет работать сервер."""
    if platform != "darwin" and platform != "win32":
        app.run(host="0.0.0.0", port=port)
    else:
        app.run(port=port)

if __name__ == '__main__':
    from application import app
    app.config.from_object('config')
    run(80)
    