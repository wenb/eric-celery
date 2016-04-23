from celery import Celery
import subprocess as sb

app = Celery('tasks', broker='amqp://guest@serveric:32771//')

app.config_from_object('celeryconfig')

@app.task(serializer='json')
def add(x,y):
    print x+y

@app.task(serializer='json')
def run_command(command):
	p = sb.Popen(command,stdin=sb.PIPE,stdout=sb.PIPE,shell=True)
	out = p.stdout.readlines()
	for line in out:
		print line.strip()

