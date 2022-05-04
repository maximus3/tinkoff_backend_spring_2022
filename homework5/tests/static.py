from database import proxy


def user_proxy_data():
    return [
        (
            proxy.UserProxy,
            {
                'username': 'username',
                'base64_string': 'dXNlcm5hbWU6cGFzc3dvcmQ=',
            },
        ),
        (
            proxy.UserProxy,
            {
                'username': 'username2',
                'base64_string': 'dXNlcm5hbWU6cGFzc3dvcmQ=',
            },
        ),
    ][:]


def movie_proxy_data():
    return [
        (
            proxy.MovieProxy,
            {
                'title': 'title 1',
                'year': 2022,
                'average_rating': 5,
                'count_ratings': 1,
                'count_reviews': 1,
            },
        ),
        (
            proxy.MovieProxy,
            {
                'title': 'title 2',
                'year': 2021,
                'average_rating': 9,
                'count_ratings': 1,
                'count_reviews': 1,
            },
        ),
        (
            proxy.MovieProxy,
            {
                'title': 'title 3',
                'year': 2021,
                'average_rating': 7,
                'count_ratings': 1,
                'count_reviews': 1,
            },
        ),
    ][:]


def review_proxy_data():
    return [
        (
            proxy.ReviewProxy,
            {
                'user_data': user_proxy_data()[0],
                'movie_data': movie_proxy_data()[0],
                'review': 'review movie 1 from user 1',
            },
        ),
        (
            proxy.ReviewProxy,
            {
                'user_data': user_proxy_data()[0],
                'movie_data': movie_proxy_data()[1],
                'review': 'review movie 2 from user 1',
            },
        ),
        (
            proxy.ReviewProxy,
            {
                'user_data': user_proxy_data()[1],
                'movie_data': movie_proxy_data()[0],
                'review': 'review movie 1 from user 2',
            },
        ),
    ][:]
