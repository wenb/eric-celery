# coding=utf-8
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def print_lines(out_put):
    for line in out_put[0:len(out_put) - 1]:
        print line.strip()