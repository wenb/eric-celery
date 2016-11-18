# encoding: utf-8

"""
@site: 
@software: PyCharm
@file: model.py.py
@time: 2016/11/17 21:56
"""

from ext import db


class Command(db.Model):
    __tablename__ = 'tab_commands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    command = db.Column(db.String(100))
    response = db.Column(db.String(1000))
    return_code = db.Column(db.Integer)

    def __init__(self, command, response,return_code):
        self.command = command
        self.response = response
        self.return_code = return_code
