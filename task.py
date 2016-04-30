from celery import Celery
from celery.signals import task_success
import subprocess as sb

app = Celery(
    'task')

app.config_from_object('celeryconfig')


@app.task
def run_command(command):
    p = sb.Popen(
        command,
        stdin=sb.PIPE,
        stdout=sb.PIPE,
        stderr=sb.PIPE,
        shell=True)
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
    print('task_success for result {result}'.format(
        result=result,
    ))
