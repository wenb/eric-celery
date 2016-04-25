from celery import Celery
# from celery.signals import task_success
import subprocess as sb

app = Celery(
    'task',
    backend='redis://serveric:32782/5',
    broker='amqp://guest@serveric:32778//')

app.config_from_object('celeryconfig')


@app.task
def run_command(command):
    p = sb.Popen(
        command,
        stdin=sb.PIPE,
        stdout=sb.PIPE,
        stderr=sb.PIPE,
        shell=True)
    out = p.stdout.readlines()
    for line in out:
        print line.strip()
    return out
