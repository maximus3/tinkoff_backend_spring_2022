import logging
import secrets

from flask import Flask

from .auth import bp_auth as auth_blueprint
from .main import bp_main as main_blueprint

logging.basicConfig(
    level=logging.INFO,
    filename='app.log',
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s',
)


def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    secret = secrets.token_urlsafe(32)
    app.secret_key = secret

    return app
