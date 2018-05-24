#!/bin/sh

mkdir -p logs

# Prepare log files and start outputting logs to stdout
touch ./logs/gunicorn.log
touch ./logs/gunicorn-access.log
tail -n 0 -f ./logs/gunicorn*.log &

export DJANGO_SETTINGS_MODULE=fweather.settings

#gunicorn fweather.wsgi:application \
gunicorn fweather.wsgi \
    --name fweather \
    --bind 0.0.0.0:8000 \
    --workers 5 \
    --log-level=info \
    --log-file=./logs/gunicorn.log \
    --access-logfile=./logs/gunicorn-access.log \
"$@"
