from werkzeug.security import generate_password_hash

from database import proxy


def user_proxy_data():
    return (
        proxy.UserProxy,
        {
            'username': 'username',
        },
    )


def user_proxy_data_password():
    return (
        proxy.UserProxy,
        {
            'username': 'username',
            'password': generate_password_hash('password', method='sha256'),
        },
    )
