CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
BROKER_URL = 'amqp://guest@serveric:32771//'
CELERY_RESULT_BACKEND = 'redis://serveric:32774/5'
BROKER_HEARTBEAT_CHECKRATE = '60s'

# Enables error emails.
# CELERY_SEND_TASK_ERROR_EMAILS = True
n
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
