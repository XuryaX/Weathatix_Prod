web: gunicorn Weathatix.wsgi --log-file -
celeryd : celery -A Weathatix worker -l info
celerybeat: celery -A Weathatix beat -l info