"""
"""

import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

here = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Load configuration.
conf_file = os.environ.get("CONFIG", None)
if not conf_file:
    raise Exception("Missing CONFIG environment variable with the configuration")
app.config.from_pyfile(conf_file)
if app.config['DEBUG']:
    app.testing = True

# Database initialization.
db = SQLAlchemy(app)
from database import models

config = app.config
