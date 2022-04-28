import logging
from typing import Any

from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

import database.views
from config import TextData
from database.status import Status as DatabaseStatus

from .utils import login_required

bp_auth = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


@bp_auth.route('/login', methods=['POST'])
def login_post() -> Any:
    username = request.cookies.get('username')
    if username:
        flash(TextData.ALREADY_LOGGED)
        return redirect(url_for('main.index'))

    login_from_form = request.form.get('login')
    if login_from_form is None:
        flash(TextData.SMTH_ERROR)
        logger.info('login_from_form is None')
        return redirect(url_for('auth.login'))
    db_status, username = database.views.create_or_exists_user(login_from_form)
    if db_status or username is None:
        if db_status != DatabaseStatus.EXISTS or username is None:
            flash(TextData.SMTH_ERROR)
            logger.info('create_or_exists_user exit with %s', db_status)
            return redirect(url_for('auth.login'))

    resp = make_response(redirect(url_for('main.index')))
    resp.set_cookie('username', username)
    return resp


@bp_auth.route('/login', methods=['GET'])
def login() -> Any:
    username = request.cookies.get('username')
    if username:
        flash(TextData.ALREADY_LOGGED)
        return redirect(url_for('main.index'))
    return render_template('login.html')


@bp_auth.route('/logout')
@login_required
def logout(_: str) -> Any:
    resp = make_response(redirect(url_for('auth.login')))
    resp.delete_cookie('username')
    return resp
