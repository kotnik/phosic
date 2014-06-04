"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
"""

import os
from flask import Flask


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '\xb0k\xd0\x03\xd9\x0b*\xa0UE\x80\x93BbIT\xa3\xe6\xef\x7fq\xf2\xf9F')
app.config['PORT'] = int(os.environ.get('PORT', 8000))
app.config['DEBUG'] = bool(os.environ.get('DEBUG', False))

# Configuration to put in file.
app.config['DEBUG'] = True
# End of configuration.

# Uploads.
here = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', os.path.join(here, 'uploads'))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

config = app.config
