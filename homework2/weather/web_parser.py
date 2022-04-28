from typing import Tuple

from bs4 import BeautifulSoup
from requests import Response

from .status import Status
from .web_getter import get_page


def get_data(page: Response) -> Tuple[Status, int]:
    soup = BeautifulSoup(page.text, 'html.parser')
    if soup.find('div', {'id': 'weather-now-number'}) is None:
        return Status.PARSE_ERROR, 0
    data = list(soup.find('div', {'id': 'weather-now-number'}).children)
    if len(data) < 1:
        return Status.PARSE_ERROR, 0
    try:
        temp = int(data[0].text)
    except ValueError:
        return Status.PARSE_ERROR, 0
    return Status.OK, temp


def get_status(page: Response) -> Status:
    if page.status_code == 200:
        return Status.OK
    if page.status_code == 404:
        return Status.ERROR_404
    return Status.ERROR


def get_temp(city: str) -> Tuple[Status, int]:
    page = get_page(city)
    status = get_status(page)
    if status != Status.OK:
        return status, 0
    status, data = get_data(page)
    return status, data
