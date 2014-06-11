import flask_app
from phosic import __all__
from phosic.utils import setup_logging

app = flask_app.app

if __name__ == '__main__':
    setup_logging(verbose=config.get('DEBUG', False), stderr=not config.get('DEBUG', False), color=True, appname="phosic")
    app.run(port=config.get('PORT'), debug=app.config.get('DEBUG', False))
