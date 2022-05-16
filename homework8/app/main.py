import secrets
from typing import Optional

from flask import Flask
from flask_login import LoginManager

from app.routers import auth, contests, main
from database.proxy import UserProxy


def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(contests.bp)

    secret = secrets.token_urlsafe(32)
    app.secret_key = secret

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[UserProxy]:
        return UserProxy.get(id=user_id)

    return app
