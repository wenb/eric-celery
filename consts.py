# coding=utf-8
HOSTNAME = 'serveric'
DATABASE = 'celerybot'
USERNAME = 'root'
PASSWORD = '123456'

RABBITMQ_URI = 'amqp://admin:{}@{}:5672//'.format(PASSWORD, HOSTNAME)
REDIS_URI = 'redis://{}:6379/0'.format(HOSTNAME)
DB_URI = 'mysql://{}:{}@{}/{}'.format(
    USERNAME, PASSWORD, HOSTNAME, DATABASE)
