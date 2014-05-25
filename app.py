"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
"""

import os
from flask import Flask


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
app.config['PORT'] = int(os.environ.get('PORT', 8000))
app.config['DEBUG'] = bool(os.environ.get('DEBUG', False))

# Configuration to put in file.
app.config['DEBUG'] = True
# End of configuration.


config = app.config
