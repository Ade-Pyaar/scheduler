web: gunicorn scheduler.wsgi --log-file -
worker: celery -A scheduler worker -B --loglevel=info
worker: celery -A scheduler beat -l INFO