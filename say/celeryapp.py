from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Setting default Django settings module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'say.settings')

app = Celery('say')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(broker_url=os.environ['REDIS_URL'], celery_result_backend=os.environ['REDIS_URL'])
app.conf.CELERY_IGNORE_RESULT = True

# Load the task modults for all Django apps
app.autodiscover_tasks()

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls say('hello') every 10 seconds.
#     sender.add_periodic_task(crontab(minute='*/15'), newsitems.tasks.retrieve_new_articles.s())
app.conf.CELERYBEAT_SCHEDULE = {
    'add-new-articles': {
        'task': 'newsitems.tasks.retrieve_new_articles',
        'schedule': crontab(minute=0, hour='*/2,*/3'),
        'args': ()
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


if __name__ == '__main__':
    app.start()
