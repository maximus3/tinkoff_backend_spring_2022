import logging
from typing import Any

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

from database.proxy import UserContestProxy

bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)


@bp.route('/')
def index() -> Any:
    if current_user.is_authenticated:
        username = current_user.username
        user_contests = UserContestProxy.get_all(user_id=current_user.id)
        return render_template(
            'index.html', login=username, user_contests=user_contests
        )
    return redirect(url_for('auth.login'))
