import database.utils


def test_normalize_money_str():
    assert database.utils.normalize_money_str('1.1') == '1.1'
    assert database.utils.normalize_money_str('1') == '1.0'
    assert database.utils.normalize_money_str('0') == '0.0'
    assert (
        database.utils.normalize_money_str('123456.000123') == '123456.000123'
    )
    assert (
        database.utils.normalize_money_str('123456.123000', strip=False) == '123456.123000'
    )
    assert database.utils.normalize_money_str('') == ''
    assert database.utils.normalize_money_str('00000') == '0.0'
    assert database.utils.normalize_money_str('00000.000100000') == '0.0001'
    assert database.utils.normalize_money_str('00001.000100000') == '1.0001'


def test_money_int_to_str():
    assert database.utils.money_int_to_str(984, 100) == '9.84'
    assert database.utils.money_int_to_str(984, 1) == '984.0'
    assert database.utils.money_int_to_str(98765, 1000) == '98.765'
    assert database.utils.money_int_to_str(0, 10) == '0.0'
    assert database.utils.money_int_to_str(0, 100) == '0.0'
    assert database.utils.money_int_to_str(1, 10000) == '0.0001'
    assert database.utils.money_int_to_str(2, 100) == '0.02'
    assert database.utils.money_int_to_str(10000001, 10000000) == '1.0000001'


def test_str_to_money():
    assert database.utils.str_to_money_tuple('984.321') == (984, 321)
    assert database.utils.str_to_money_tuple('984.0') == (984, 0)
    assert database.utils.str_to_money_tuple('0.3') == (0, 3)
    assert database.utils.str_to_money_tuple('0.0') == (0, 0)
    assert database.utils.str_to_money_tuple('0.12') == (0, 12)
    assert database.utils.str_to_money_tuple('0.1') == (0, 1)


def test_str_to_money_tuple_one():
    assert database.utils.str_to_money_tuple('984') == (984, 0)
    assert database.utils.str_to_money_tuple('0') == (0, 0)


def test_str_to_money_tuple_zero_after():
    assert database.utils.str_to_money_tuple('984.123000') == (984, 123000)
    assert database.utils.str_to_money_tuple('0.1000000') == (0, 1000000)


def test_str_to_money_tuple_many_zero_before():
    assert database.utils.str_to_money_tuple('984.000123') == (984, 123)
    assert database.utils.str_to_money_tuple('0.000001') == (0, 1)
    assert database.utils.str_to_money_tuple('984.123000') == (984, 123000)
    assert database.utils.str_to_money_tuple('0.100000') == (0, 100000)


def test_min_nanos_zero():
    assert database.utils.min_nanos_zero('5.984', '1234.321') == 3
    assert database.utils.min_nanos_zero('2143.984', '0.3') == 3
    assert database.utils.min_nanos_zero('213.123456', '1.3') == 6
    assert database.utils.min_nanos_zero('0.123456', '0.123456789') == 9
    assert database.utils.min_nanos_zero('0.12', '0.1') == 2


def test_prepare_op_str():
    assert database.utils.prepare_op_str('5.984', '1234.321') == (
        5984,
        1234321,
        1000,
    )
    assert database.utils.prepare_op_str('2143.984', '0.3') == (
        2143984,
        300,
        1000,
    )
    assert database.utils.prepare_op_str('213.123456', '1.3') == (
        213123456,
        1300000,
        1000000,
    )
    assert database.utils.prepare_op_str('0.123456', '0.123456789') == (
        123456000,
        123456789,
        1000000000,
    )
    assert database.utils.prepare_op_str('0.12', '0.1') == (12, 10, 100)


def test_op_str_mul():
    assert database.utils.op_str_mul('5.984', '1234.321') == '7386.176864'
    assert database.utils.op_str_mul('2143.984', '0.3') == '643.1952'
    assert database.utils.op_str_mul('213.123456', '1.3') == '277.0604928'
    assert (
        database.utils.op_str_mul('0.123456', '0.123456789')
        == '0.015241481342784'
    )
    assert database.utils.op_str_mul('213.123456', '0.0') == '0.0'


def test_op_str_add():
    assert database.utils.op_str_add('5.984', '1234.321') == '1240.305'
    assert database.utils.op_str_add('2143.984', '0.3') == '2144.284'
    assert database.utils.op_str_add('213.123456', '1.3') == '214.423456'
    assert (
        database.utils.op_str_add('0.123456', '0.123456789') == '0.246912789'
    )
    assert database.utils.op_str_add('213.123456', '0.0') == '213.123456'


def test_op_str_sub():
    assert database.utils.op_str_sub('1234.321', '5.984') == '1228.337'
    assert database.utils.op_str_sub('2143.984', '0.3') == '2143.684'
    assert database.utils.op_str_sub('213.123456', '1.3') == '211.823456'
    assert database.utils.op_str_sub('0.12', '0.1') == '0.02'
    assert (
        database.utils.op_str_sub('0.123456789', '0.123456') == '0.000000789'
    )
    assert database.utils.op_str_sub('213.123456', '0.0') == '213.123456'
