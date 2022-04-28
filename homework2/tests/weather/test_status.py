from weather.status import Status


def test_status_ok():
    assert Status.OK == 0


def test_status_error_404():
    assert Status.ERROR_404 > 0


def test_status_error():
    assert Status.ERROR > 0


def test_status_parse_error():
    assert Status.PARSE_ERROR > 0
