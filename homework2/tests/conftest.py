import pytest


@pytest.fixture()
def page_ok(mocker):
    mock = mocker.MagicMock()
    mock.status_code = 200
    mock.text = '<div id=weather-now-number>20</div>'
    return mock


@pytest.fixture()
def page_ok_minus(mocker):
    mock = mocker.MagicMock()
    mock.status_code = 200
    mock.text = '<div id=weather-now-number>-20</div>'
    return mock


@pytest.fixture()
def page_broken_no_int(mocker):
    mock = mocker.MagicMock()
    mock.status_code = 200
    mock.text = '<div id=weather-now-number>qwerty</div>'
    return mock


@pytest.fixture()
def page_broken_no_div(mocker):
    mock = mocker.MagicMock()
    mock.status_code = 200
    mock.text = '<a>20</a>'
    return mock


@pytest.fixture()
def page_broken_div_no_child(mocker):
    mock = mocker.MagicMock()
    mock.status_code = 200
    mock.text = '<div id=weather-now-number></div>'
    return mock


@pytest.fixture()
def page_404(mocker):
    mock = mocker.MagicMock()
    mock.status_code = 404
    return mock


@pytest.fixture()
def page_err(mocker):
    mock = mocker.MagicMock()
    mock.status_code = 500
    return mock


@pytest.fixture()
def requests_mock(mocker):
    return mocker.patch('requests.get')
