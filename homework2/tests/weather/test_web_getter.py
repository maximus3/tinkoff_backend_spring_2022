import requests

from config import ConfigData
from weather.web_getter import get_page


def test_get_page(requests_mock):
    get_page('moscow')
    requests.get.assert_called_once_with(ConfigData.SITE.format('moscow'))
