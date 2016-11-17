#!/usr/bin/env bash
# celery -A task worker -l DEBUG -Ofair
celery -A celery_socketio.celery -P eventlet worker -l info