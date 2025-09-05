#!/bin/bash
# Скрипт для миграций на Render
python manage.py migrate
python manage.py collectstatic --noinput
