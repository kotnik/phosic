"""
"""

import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

here = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '\xb0k\xd0\x03\xd9\x0b*\xa0UE\x80\x93BbIT\xa3\xe6\xef\x7fq\xf2\xf9F')
app.config['PORT'] = int(os.environ.get('PORT', 8000))
app.config['DEBUG'] = bool(os.environ.get('DEBUG', False))

# Configuration to put in file.
app.config['DEBUG'] = True
if app.config['DEBUG']:
    app.testing = True
# End of configuration.

# Uploads.
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', os.path.join(here, 'uploads'))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Recapthca.
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcrufQSAAAAALwUQKlvx2YKvMIQZ1mabsOgxTJR'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcrufQSAAAAAEfnYns8o-LPGjlD0s6u6veYWEc0'

# Database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(here, 'app.db')
app.config['SQLALCHEMY_MIGRATE_REPO'] = os.path.join(here, 'db_repository')
db = SQLAlchemy(app)
from database import models

config = app.config
