# coding=utf-8
from __future__ import unicode_literals
from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet
from celery import Celery
from celery.signals import task_success
from celery.result import AsyncResult
# from celery.execute import send_task
from subprocess import *
import os
import sys
import logging
import time
from ext import *
from model import Command
import json

environ = os.environ.copy()
local_coding = sys.stdout.encoding
assert local_coding
eventlet.monkey_patch()

here = os.path.abspath(os.path.dirname(__file__))
templates_path = os.path.join(here, "templates")
static_path = os.path.join(here, "static")

app = Flask(__name__, template_folder=templates_path,static_folder=static_path)
app.config.from_pyfile(os.path.join(here, 'celeryconfig.py'))
app.config.update()

db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

SOCKETIO_REDIS_URL = app.config['CELERY_RESULT_BACKEND']
socketio = SocketIO(
    app, async_mode='eventlet',
    message_queue=SOCKETIO_REDIS_URL)

celery = Celery(app.name)
celery.conf.update(app.config)


@celery.task
def background_task():
    socketio.emit(
        'my response', {'data': 'Task starting ...'},
        namespace='/task')
    time.sleep(10)
    socketio.emit(
        'my response', {'data': 'Task complete!'},
        namespace='/task')


@celery.task
def async_task():
    print 'Async!'
    time.sleep(5)


@celery.task
def celery_run_command(command):
    kwargs = {'shell': True, 'stdout': PIPE, 'stderr': PIPE, 'stderr': PIPE, 'env': environ}
    p = Popen(command, **kwargs)
    p.wait()
    out = p.stdout.readlines()
    for line in out:
        print line.strip()
    # out.append(str(p.returncode))
    logging.info(str(p.returncode))
    return out


@celery.task(bind=True)
def error_handler(self, uuid):
    result = self.app.AsyncResult(uuid)
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
          uuid, result.result, result.traceback))


@task_success.connect()
def handler_task_success(send=None, result=None, **kwargs):
    pass


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/async')
def async():
    async_task.delay()
    return 'Task complete!'


@app.route('/task')
def start_background_task():
    background_task.delay()
    return 'Started'


@app.route('/command')
def run_command(command="ls"):
    output = celery_run_command.delay(command)
    response = AsyncResult(output.task_id).get()
    json_output = json.dumps(response)
    # icommand = Command(command, response, output.status)
    # db.session.add(icommand)
    # db.session.commit()
    logging.info(str(output))
    return json_output


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9000, debug=True)
