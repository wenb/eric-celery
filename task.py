from celery import Celery
import subprocess as sb

app = Celery('task',backend='redis://serveric:32774/5',broker='amqp://guest@serveric:32771//')

app.config_from_object('celeryconfig')

@app.task
def add(x,y):
    print x+y

@app.task
def run_command(command):
	p = sb.Popen(command,stdin=sb.PIPE,stdout=sb.PIPE,shell=True)
	out = p.stdout.readlines()
	for line in out:
		print line.strip()

