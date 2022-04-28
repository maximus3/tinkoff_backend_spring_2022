from typing import Optional

from .models import Currency, Operation, User, UserCurrency


class CurrencyProxy:
    def __init__(
        self, name: str, rate: str, count: Optional[str] = None
    ) -> None:
        self.name = name
        self.rate = rate
        self.count = count

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.rate == other.rate and self.count == other.count


class OperationProxy:
    def __init__(self, operation: Operation, currency_name: str) -> None:
        self.type = operation.type
        self.currency = currency_name
        self.count = operation.count
        self.rate = operation.rate
        self.money = operation.money

    def __eq__(self, other):
        return self.type == other.type and self.currency == other.currency and self.count == other.count and self.rate == other.rate and self.money == other.money


class BuySellModelsProxy:
    def __init__(
        self,
        user: User,
        money_currency: Currency,
        money_user_currency: UserCurrency,
        currency: Currency,
        user_currency: UserCurrency,
    ) -> None:
        self.user = user
        self.money_currency = money_currency
        self.money_user_currency = money_user_currency
        self.currency = currency
        self.user_currency = user_currency

    def __eq__(self, other):
        return self.user == other.user and self.money_currency == other.money_currency and self.money_user_currency == other.money_user_currency and self.currency == other.currency and self.user_currency == other.user_currency
