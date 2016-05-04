# -*- coding: utf-8 -*-
__version__ = '1.9.1'

import os, sys
import ConfigParser
import socket
import psutil
import platform
from subprocess import Popen, PIPE

from celery import Celery
from celery.execute import send_task
from celery.utils.log import get_task_logger
from celery.utils.dispatch import Signal
from celery.signals import task_success, task_failure, worker_ready

if psutil.__version__.split('.')[0] == '1':
    psutil_children_method_name = 'get_children'
else:
    psutil_children_method_name = 'children'

logger = get_task_logger(__name__)
local_encoding = sys.stdout.encoding
assert local_encoding


def init_config():
    # try ini file in current folder
    ini_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meta.ini')
    if not os.path.isfile(ini_config):
        print 'no meta file found'
        exit(-1)

    ini_parser = ConfigParser.SafeConfigParser()
    ini_parser.read(ini_config)
    meta_items = dict(ini_parser.items('meta', raw=True))

    TENANT = meta_items.get('quantbot_tenant')
    MQ_HOST = meta_items.get('quantbot_mq_host')
    MQ_PORT = meta_items.get('quantbot_mq_port', 5672)
    MQ_USER = meta_items.get('quantbot_mq_user')
    MQ_PASSWD = meta_items.get('quantbot_mq_passwd')
    UUID = meta_items.get('quantbot_uuid')

    assert TENANT
    assert MQ_HOST
    assert MQ_USER
    assert MQ_PASSWD
    assert UUID

    broker = 'amqp://%s:%s@%s:%s//' % (MQ_USER, MQ_PASSWD, MQ_HOST, MQ_PORT)
    queue = 'qb-agent.%s@%s' % (UUID, socket.gethostname())
    routing_key = UUID

    config_object = dict(
        BROKER_URL=broker,
        CELERY_DEFAULT_QUEUE=queue,
        CELERY_DEFAULT_EXCHANGE="quantbot",
        CELERY_DEFAULT_EXCHANGE_TYPE="direct",
        CELERY_DEFAULT_ROUTING_KEY=routing_key,
        CELERY_TIMEZONE='UTC',
        CELERY_ENABLE_UTC=True,
        CELERY_ACKS_LATE=True,
        CELERYD_PREFETCH_MULTIPLIER=1,
        CELERYD_MAX_TASKS_PER_CHILD=50,
        BROKER_TRANSPORT_OPTIONS={'confirm_publish': True}
    )

    return config_object, meta_items


app = Celery('quantbot')
config, meta = init_config()
app.config_from_object(config)


### Task definitions 

@app.task(bind=True, ignore_result=True)
def start_task(self, command, env={}):
    sender = '%s.%s' % (self.__module__, self.__name__)
    task_id = self.request.id

    environ = os.environ.copy()
    environ.update(env)

    kwargs = {'shell': True, 'stdout': PIPE, 'stderr': PIPE, 'env': environ}
    proc = Popen(command.encode(local_encoding), **kwargs)

    qb_task_started.send(sender=sender, body=None, task_id=task_id, pid=proc.pid)
    stdout_data, stderr_data = proc.communicate()

    result = [task_id, proc.returncode, stdout_data, stderr_data]
    qb_task_completed.send(sender=sender, body=None, result=result)
    return proc.returncode


@app.task(ignore_result=True)
def kill_task(task_id, pid):
    def kill_process(p):
        try:
            p.kill()
        except psutil.NoSuchProcess:
            pass

    if not psutil.pid_exists(pid):
        return task_id, False

    process = psutil.Process(pid)
    processes = getattr(process, psutil_children_method_name)(recursive=True)
    processes.append(process)

    [kill_process(p) for p in processes]

    return task_id, True


@app.task(ignore_result=True)
def update_script():
    # TODO need to download the script
    # TODO need to restart this process
    pass


### Signal Definitions
qb_task_started = Signal(providing_args=['task_id', 'pid'])
qb_task_completed = Signal(providing_args=['result'])
qb_task_killed = Signal(providing_args=['result'])


### Signal hanlders
@worker_ready.connect
def register_host(sender=None, body=None, **kwargs):
    """
    send a host register message to quantbot controller when worker ready.
    it should be only send one time during a life cycle of a worker.
    """

    def get_agent_ip(host):
        """
        get agent IP which one connect to mq host.
        :param host:
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((host, 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    args = [
        socket.gethostname().strip(),
        get_agent_ip(meta.get('quantbot_mq_host')),
        platform.system().lower(),
        meta.get('quantbot_tenant'),
        meta.get('quantbot_uuid')
    ]
    send_task('tasks.host_register', args=args, routing_key='report')


@qb_task_started.connect  # (sender='quantbotagent.start_task')
def task_started_handler(sender=None, body=None, **kwargs):
    send_task('tasks.task_started', args=[kwargs['task_id'], kwargs['pid']], routing_key='report')


@qb_task_completed.connect
def task_completed_handler(sender=None, body=None, **kwargs):
    send_task('tasks.task_completed', args=kwargs['result'], routing_key='report')


@task_success.connect(sender='quantbotagent.kill_task')
def task_success_handler(sender=None, body=None, **kwargs):
    send_task('tasks.task_killed', args=kwargs['result'], routing_key='report')


@task_failure.connect
def task_failure_handler(sender=None, body=None, **kwargs):
    einfo = kwargs.get('einfo', None)
    send_task('tasks.task_exception', args=[kwargs['task_id'], einfo.traceback], routing_key='report')
