import datetime as dt
from typing import Any, List, Union


class Record:
    '''Конструктор класса, который используется для инициализации переменных.
    amount - (денежная сумма или количество килокалорий),
    comment - (комментарий поясняющий,
    на что потрачены деньги или откуда взялись калории),
    date - (дата передаётся в явном виде в конструктор,
    либо присваивается значение по умолчанию — текущая дата).'''
    def __init__(self, amount: Union[int, float],
                 comment: str, date: str = None) -> None:
        self.amount = amount
        self.comment = comment
        date_format = '%d.%m.%Y'
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator:
    '''Конструктор класса,
    который используется для инициализации переменных.
    limit - (дневной лимит трат/калорий, который задал пользователь)
    records - (пустой список, в котором хранятся записи).'''
    def __init__(self, limit: Union[int, float]) -> None:
        self.records: List[Any] = []
        self.limit = limit

    '''Этот метод сохраняет новую запись о расходах/приёме пищи.'''
    def add_record(self, obj: Record) -> None:
        self.records.append(obj)

    '''Этот метод считает,
    сколько было денег потрачено/калорий съедено сегодня.'''
    def get_today_stats(self) -> Union[int, float]:
        today = dt.date.today()
        counter_today: Union[int, float] = 0
        for i in self.records:
            if i.date == today:
                counter_today = sum([i.amount], counter_today)
        return counter_today

    '''Этот метод считает,
    сколько денег потрачено/калорий получено за последние 7 дней.'''
    def get_week_stats(self) -> Union[int, float]:
        week = dt.timedelta(weeks=1)
        counter_week: Union[int, float] = 0
        for i in self.records:
            if (dt.date.today() >= i.date > (dt.date.today() - week)):
                counter_week = sum([i.amount], counter_week)
        return counter_week


class CaloriesCalculator(Calculator):
    '''Этот метод вычисляет, сколько калорий вы можете съесть сегодня.'''
    def get_calories_remained(self) -> str:
        if self.get_today_stats() < self.limit:
            remains_calories = self.limit - self.get_today_stats()
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{remains_calories} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE: float = 73.59
    EURO_RATE: float = 87.98
    RUB_RATE: float = 1

    '''Этот метод вычисляет, сколько денег осталось на сегодняшний день.'''
    def get_today_cash_remained(self, currency: str) -> str:
        currency_info = {
            'rub': ('руб', self.RUB_RATE),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
        }

        limit_rate = (abs(self.limit - self.get_today_stats()))
        currency_name, currency_rate = currency_info[currency]
        remains_cash = round(limit_rate / currency_rate, 2)

        if self.get_today_stats() < self.limit:
            return f'На сегодня осталось {remains_cash} {currency_name}'
        elif self.get_today_stats() > self.limit:
            return ('Денег нет, держись: '
                    f'твой долг - {remains_cash} {currency_name}')
        return 'Денег нет, держись'
