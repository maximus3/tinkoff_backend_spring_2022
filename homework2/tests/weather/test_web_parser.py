from weather.status import Status
from weather.web_parser import get_data, get_status, get_temp


def test_get_data_ok(page_ok):
    assert get_data(page_ok) == (Status.OK, 20)


def test_get_data_ok_minus(page_ok_minus):
    assert get_data(page_ok_minus) == (Status.OK, -20)


def test_get_data_err_no_div(page_broken_no_div):
    assert get_data(page_broken_no_div) == (Status.PARSE_ERROR, 0)


def test_get_data_err_div_no_child(page_broken_div_no_child):
    assert get_data(page_broken_div_no_child) == (Status.PARSE_ERROR, 0)


def test_get_data_err_no_int(page_broken_no_int):
    assert get_data(page_broken_no_int) == (Status.PARSE_ERROR, 0)


def test_get_status_ok(page_ok):
    assert get_status(page_ok) == Status.OK


def test_get_status_404(page_404):
    assert get_status(page_404) == Status.ERROR_404


def test_get_status_err(page_err):
    assert get_status(page_err) == Status.ERROR


def test_get_temp_ok(requests_mock, page_ok):
    requests_mock.return_value.status_code = 200
    requests_mock.return_value.text = page_ok.text
    assert get_temp('moscow') == (Status.OK, 20)


def test_get_temp_ok_minus(requests_mock, page_ok_minus):
    requests_mock.return_value.status_code = 200
    requests_mock.return_value.text = page_ok_minus.text
    assert get_temp('moscow') == (Status.OK, -20)


def test_get_temp_err(requests_mock, page_404):
    requests_mock.return_value.status_code = 404
    requests_mock.return_value.text = page_404.text
    assert get_temp('moscowq') == (Status.ERROR_404, 0)
