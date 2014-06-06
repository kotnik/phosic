from app import app, config
from phosic import __all__

if __name__ == '__main__':
    app.run(port=config.get('PORT'), debug=config.get('DEBUG', False))
