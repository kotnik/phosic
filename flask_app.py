"""
"""

import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from celery import Celery

def make_app():
    app = Flask(__name__)

    # Load configuration.
    conf_file = os.environ.get("CONFIG", None)
    if not conf_file:
        raise Exception("Missing CONFIG environment variable with the configuration")
    app.config.from_pyfile(conf_file)
    if app.config['DEBUG']:
        app.testing = True

    return app

# Celery.
def make_celery(app=None):
    if not app:
        app = make_app()
    celery = Celery('tasks', broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

# Flask application.
app = make_app()

# Celery.
celery = make_celery(app)

# Database initialization.
db = SQLAlchemy(app)
from database import models

config = app.config
