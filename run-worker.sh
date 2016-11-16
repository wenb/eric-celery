#!/usr/bin/env bash
celery -A task worker -l DEBUG -Ofair