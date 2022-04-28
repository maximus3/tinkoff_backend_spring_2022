from collections import defaultdict
from typing import Dict

from config import TextData

from .status import Status

status_to_text: Dict[Status, str] = defaultdict(
    lambda: TextData.STATUS_NOT_FOUND
)
status_to_text_default: Dict[Status, str] = {
    Status.OK: TextData.WEATHER_TEXT,
    Status.ERROR_404: TextData.ERROR_404,
    Status.ERROR: TextData.ERROR,
    Status.PARSE_ERROR: TextData.PARSE_ERROR,
}
status_to_text.update(status_to_text_default)


def get_message(city: str, status: Status, data: int) -> str:
    return status_to_text[status].format(city, data)
