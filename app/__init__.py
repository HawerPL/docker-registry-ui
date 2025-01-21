import os
import logging
from datetime import timedelta
from logging.handlers import RotatingFileHandler
from urllib.parse import quote_plus

import babel
from flask import Flask, session
from flask_babel import Babel
from flask_login import LoginManager
from app.config import Config


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'dev'
    app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)

    login_manager = LoginManager()
    login_manager.init_app(app)

    if app.config['ENABLED_AUTH']:
        login_manager.login_view = 'app.login'
        app.config['LOGIN_DISABLED'] = False
    else:
        app.config['LOGIN_DISABLED'] = True

    config_logger(app)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=app.config['SESSION_TIME'])
    app.config['BABEL_DEFAULT_LOCALE'] = Config.DEFAULT_LOCALE

    from app.routes import app_routes
    app.register_blueprint(app_routes.bp, url_prefix="/")

    from app.routes import registry_routes
    app.register_blueprint(registry_routes.bp, url_prefix="/registry")

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import users
        return next((user for user in users if user.user_id == int(user_id)), None)

    def get_locale():
        return session.get('language', app.config['BABEL_DEFAULT_LOCALE'])

    babel_i18n = Babel(app, locale_selector=get_locale)

    return app


def config_logger(app):
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    os.makedirs('logs', exist_ok=True)
    file_handler = RotatingFileHandler(os.path.join('logs', 'app.log'), maxBytes=10240, backupCount=10)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(app.config['LOG_LEVEL'])

    app.logger.addHandler(file_handler)
    app.logger.setLevel(app.config['LOG_LEVEL'])

    # logger = logging.getLogger('werkzeug')
    # handler = file_handler
    # logger.addHandler(handler)


