def normalize_money_str(money_str: str, strip: bool = True) -> str:
    if not money_str:
        return money_str
    if len(money_str.split('.')) == 1:
        money_str = money_str + '.0'
    if strip:
        money_str = money_str.strip('0')
        if money_str[0] == '.':
            money_str = '0' + money_str
        if money_str[-1] == '.':
            money_str = money_str + '0'
    return money_str


def money_int_to_str(res: int, pow_10: int) -> str:
    idx = len(str(pow_10)) - 1
    str_res = '0' * idx + str(res)
    if idx == 0:
        money_str = f'{res}.0'.strip('0')
    else:
        money_str = f'{str_res[:-idx]}.{str_res[-idx:]}'.strip('0')
    return normalize_money_str(money_str)


def str_to_money_tuple(money: str) -> tuple[int, ...]:
    return tuple(map(int, normalize_money_str(money, strip=False).split('.')))


def min_nanos_zero(str_1: str, str_2: str) -> int:
    return max(len(str(str_1.split('.')[1])), len(str(str_2.split('.')[1])))


def prepare_op_str(x: str, y: str) -> tuple[int, int, int]:
    x, y = normalize_money_str(x), normalize_money_str(y)
    zero_count = min_nanos_zero(x, y)
    pow_10 = 10**zero_count
    x_list = x.split('.')
    y_list = y.split('.')
    x_new = (
        x_list[0]
        + '.'
        + x_list[1]
        + '0' * max(0, (zero_count - len(x_list[1])))
    )
    y_new = (
        y_list[0]
        + '.'
        + y_list[1]
        + '0' * max(0, (zero_count - len(y_list[1])))
    )
    x_list_new = str_to_money_tuple(x_new)
    y_list_new = str_to_money_tuple(y_new)
    x_int = x_list_new[0] * pow_10 + x_list_new[1]
    y_int = y_list_new[0] * pow_10 + y_list_new[1]
    return x_int, y_int, pow_10


def op_str_mul(x: str, y: str) -> str:
    x_int, y_int, pow_10 = prepare_op_str(x, y)
    res = x_int * y_int
    return money_int_to_str(res, pow_10 * pow_10)


def op_str_add(x: str, y: str) -> str:
    x_int, y_int, pow_10 = prepare_op_str(x, y)
    res = x_int + y_int
    return money_int_to_str(res, pow_10)


def op_str_sub(x: str, y: str) -> str:
    x_int, y_int, pow_10 = prepare_op_str(x, y)
    res = x_int - y_int
    return money_int_to_str(res, pow_10)
