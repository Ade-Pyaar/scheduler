web: gunicorn scheduler.wsgi --log-file -
worker: celery -A scheduler worker -l info -B