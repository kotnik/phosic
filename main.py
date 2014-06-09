from flask_app import app, config
from phosic import __all__
from phosic.utils import setup_logging

if __name__ == '__main__':
    setup_logging(verbose=config.get('DEBUG', False), stderr=not config.get('DEBUG', False), color=True, appname="phosic")
    app.run(port=config.get('PORT'), debug=config.get('DEBUG', False))
