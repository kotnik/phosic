from celery import Celery

from flask_app import make_celery, db

# celery = Celery('tasks')
celery = make_celery()
celery.config_from_object('celery_config')

@celery.task()
def calculate_statistics(x, y):
    return x + y

@celery.task()
def make_video():
    return True
