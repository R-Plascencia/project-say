web: gunicorn say.wsgi:application --log-file -
main_worker: celery -A say.celeryapp beat -l info
worker: celery worker -A say.celeryapp
