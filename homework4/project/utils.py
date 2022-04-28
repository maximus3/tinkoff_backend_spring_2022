from functools import wraps
from typing import Any, Callable

from flask import flash, redirect, request, url_for

from config import TextData


def login_required(func: Callable[[str], Any]) -> Callable[[], Any]:
    @wraps(func)
    def decorated_view() -> Any:
        username = request.cookies.get('username')
        if username:
            return func(username)
        flash(TextData.LOGIN_REQU)
        return redirect(url_for('auth.login'))

    return decorated_view
