from config import TextData
from weather.status import Status
from weather.utils import get_message


def test_get_message_status_ok():
    assert get_message(
        'moscow', Status.OK, -5
    ) == TextData.WEATHER_TEXT.format('moscow', -5)


def test_get_message_status_error_404():
    assert get_message(
        'moscowwef', Status.ERROR_404, -5
    ) == TextData.ERROR_404.format('moscowwef')


def test_get_message_status_error():
    assert get_message('moscow', Status.ERROR, -5) == TextData.ERROR


def test_get_message_status_parse_error():
    assert (
        get_message('moscow', Status.PARSE_ERROR, -5) == TextData.PARSE_ERROR
    )
