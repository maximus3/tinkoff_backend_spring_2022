import requests

from config import ConfigData


def get_page(city: str) -> requests.Response:
    return requests.get(ConfigData.SITE.format(city))
