# _*_coding_*_ = utf-8
from consts import DB_URI

DEBUG = True
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
BROKER_URL = 'amqp://admin:123456@serveric:5672//'
CELERY_RESULT_BACKEND = 'redis://serveric:6379/0'
BROKER_HEARTBEAT_CHECKRATE = '60s'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24

# Enables error emails.
# CELERY_SEND_TASK_ERROR_EMAILS = True

# # Name and email addresses of recipients
# ADMINS = (
#     ('eric feng', 'fengeric0910@163.com'),
# )

# # Email address used as sender (From field).
# SERVER_EMAIL = 'fengeric0910@163.com'

# # Mailserver configuration
# EMAIL_HOST = 'mail.163.com'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = 'fengeric0910@163.com'
# EMAIL_HOST_PASSWORD = 'f1w9b88bb'
