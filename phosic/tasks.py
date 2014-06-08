from flask_app import make_celery, db

celery = make_celery()

@celery.task()
def calculate_statistics(x, y):
    return x + y

@celery.task()
def make_video():
    return True
