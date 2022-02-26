web: gunicorn scheduler.wsgi --log-file -
celery: celery -A scheduler worker --pool=solo -l info
celery: celery -A scheduler beat -l INFO