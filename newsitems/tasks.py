from __future__ import absolute_import, unicode_literals
from celery import shared_task
from newsitems.utils import populate_newsitems
from say.celeryapp import app

@app.task
def retrieve_new_articles():
    print('Populating items now...')
    populate_newsitems()
