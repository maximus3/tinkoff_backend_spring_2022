import logging
from typing import Any

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.utils import login_required, no_login_required
from config.text import TextData
from database.proxy import UserProxy

bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


@bp.route('/signup', methods=['POST'])
@no_login_required
def signup_post() -> Any:
    login_from_form = request.form.get('login')
    if login_from_form is None:
        flash(TextData.SMTH_ERROR)
        logger.info('login_from_form is None')
        return redirect(url_for('auth.signup'))
    password = request.form.get('password')
    if password is None:
        flash(TextData.SMTH_ERROR)
        logger.info('password is None')
        return redirect(url_for('auth.signup'))
    user = UserProxy.get(username=login_from_form)
    if user is not None:
        flash(TextData.USER_EXISTS)
        logger.info('user exists')
        return redirect(url_for('auth.signup'))
    UserProxy.create(
        username=login_from_form,
        password=generate_password_hash(password, method='sha256'),
    )

    return redirect(url_for('auth.login'))


@bp.route('/signup', methods=['GET'])
@no_login_required
def signup() -> Any:
    return render_template('signup.html')


@bp.route('/login', methods=['GET'])
@no_login_required
def login() -> Any:
    return render_template('login.html')


@bp.route('/login', methods=['POST'])
@no_login_required
def login_post() -> Any:
    login_from_form = request.form.get('login')
    if login_from_form is None:
        flash(TextData.SMTH_ERROR)
        logger.info('login_from_form is None')
        return redirect(url_for('auth.login'))
    password = request.form.get('password')
    if password is None:
        flash(TextData.SMTH_ERROR)
        logger.info('password is None')
        return redirect(url_for('auth.login'))
    remember = bool(request.form.get('remember'))

    user = UserProxy.get(username=login_from_form)
    if user is None or not check_password_hash(user.password, password):
        flash(TextData.LOGIN_FAILED)
        logger.info('user is None or not check_password_hash')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.index'))


@bp.route('/logout')
@login_required
def logout() -> Any:
    logout_user()
    return redirect(url_for('auth.login'))
