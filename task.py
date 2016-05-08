from celery import Celery
from celery.signals import task_success
# from celery.execute import send_task
import sys

local_coding = sys.stdout.encoding
assert local_coding

app = Celery(
    'task')

app.config_from_object('celeryconfig')


@app.task
def run_command(command):
    kwargs = {'shell': True, 'stdout': PIPE, 'stderr': PIPE, 'stderr':PIPE,'env': environ}
    p = Popen(command.encoding(local_coding),**kwargs)
    p.wait()
    out = p.stdout.readlines()
    for line in out:
        print line.strip()
    out.append(str(p.returncode))
    return out


@app.task(bind=True)
def error_handler(self, uuid):
    result = self.app.AsyncResult(uuid)
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
          uuid, result.result, result.traceback))


@task_success.connect()
def handler_task_success(send=None, result=None, **kwargs):
    send_task()
