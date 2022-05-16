from functools import wraps
from typing import Any

from flask import flash, redirect, url_for
from flask_login import current_user

from config.text import TextData


def login_required(func):  # type: ignore
    @wraps(func)
    def decorated_view(
        *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Any:
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        flash(TextData.LOGIN_REQU)
        return redirect(url_for('auth.login'))

    return decorated_view


def no_login_required(func):  # type: ignore
    @wraps(func)
    def decorated_view(
        *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Any:
        if current_user.is_authenticated:
            flash(TextData.ALREADY_LOGGED)
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)

    return decorated_view
