from database.status import Status


def test_status_ok():
    assert Status.OK == 0


def test_status_exists():
    assert Status.EXISTS > 0


def test_status_time_exp():
    assert Status.TIME_EXP > 0


def test_status_no_money():
    assert Status.NO_MONEY > 0
