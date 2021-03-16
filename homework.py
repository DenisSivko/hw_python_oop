import datetime as dt
from typing import List, Union


class Record:
    def __init__(self, amount: Union[int, float],
                 comment: str, date: str = None) -> None:
        """
        Инициализирует переменные.
        amount - (денежная сумма или количество килокалорий),
        comment - (комментарий поясняющий,
        на что потрачены деньги или откуда взялись калории),
        date - (дата передаётся в явном виде в конструктор,
        либо присваивается значение по умолчанию — текущая дата).
        """
        self.amount = amount
        self.comment = comment
        date_format = '%d.%m.%Y'
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator:
    def __init__(self, limit: Union[int, float]) -> None:
        """
        Инициализирует переменные.
        limit - (дневной лимит трат/калорий, который задал пользователь)
        records - (пустой список, в котором хранятся записи).
        """
        self.records: List[Record] = []
        self.limit = limit

    def add_record(self, obj: Record) -> None:
        """Сохраняет новую запись о расходах/приёме пищи."""
        self.records.append(obj)

    def get_today_stats(self) -> Union[int, float]:
        """Считает, сколько было денег потрачено/калорий съедено сегодня."""
        today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == today)

    def get_week_stats(self) -> Union[int, float]:
        """
        Считает, сколько денег потрачено/калорий получено за последние 7 дней.
        """
        week = dt.timedelta(weeks=1)
        today = dt.date.today()
        week_ago = today - week
        return sum(record.amount for record in self.records
                   if today >= record.date > week_ago)

    def get_remains(self) -> Union[int, float]:
        """Вычисляет остаток денег/калорий за сегодня."""
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        """Вычисляет, сколько калорий вы можете съесть сегодня."""
        remains_calories = super().get_remains()
        if remains_calories > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{remains_calories} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE: float = 73.59
    EURO_RATE: float = 87.98
    RUB_RATE: float = 1

    def get_today_cash_remained(self, currency: str) -> str:
        """Вычисляет, сколько денег осталось на сегодняшний день."""
        currency_info = {
            'rub': ('руб', self.RUB_RATE),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
        }

        if currency not in currency_info:
            raise ValueError('Данной валюты нет в словаре')

        limit_rate = super().get_remains()
        if limit_rate == 0:
            return 'Денег нет, держись'

        currency_name, currency_rate = currency_info[currency]
        remains_cash = round(abs(limit_rate) / currency_rate, 2)

        if limit_rate > 0:
            return f'На сегодня осталось {remains_cash} {currency_name}'
        else:
            return ('Денег нет, держись: '
                    f'твой долг - {remains_cash} {currency_name}')
