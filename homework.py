import datetime as dt
from typing import Any, List


class Record:
    def __init__(self, amount: float, comment: str, date=None):
        self.amount = amount
        self.comment = comment
        date_format = '%d.%m.%Y'
        if date is None:
            now = dt.datetime.now()
            self.date = now.date()
        else:
            moment = dt.datetime.strptime(date, date_format)
            self.date = moment.date()


class Calculator:
    def __init__(self, limit: float):
        records: List[Any] = []
        self.records = records
        self.limit = limit
        counter_today: float = 0
        self.counter_today = counter_today
        counter_week: float = 0
        self.counter_week = counter_week

    def add_record(self, obj: Record):
        self.records.append(obj)
        print(self.records)

    def get_today_stats(self):
        for i in self.records:
            if i.date == dt.date.today():
                self.counter_today += i.amount
        print(self.counter_today)
        return self.counter_today

    def get_week_stats(self):
        week = dt.timedelta(weeks=1)
        for i in self.records:
            if (dt.date.today() >= i.date > (dt.date.today() - week)):
                self.counter_week += i.amount
        print(self.counter_week)
        return self.counter_week


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.get_today_stats() < self.limit:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{self.limit - self.counter_today} кКал')
        else:
            return f"{'Хватит есть!'}"


class CashCalculator(Calculator):
    USD_RATE: float = 73.59
    EURO_RATE: float = 87.98
    RUB_RATE: float = 1

    def get_today_cash_remained(self, currency: str):
        currency_info = {
            'rub': ['руб', self.RUB_RATE],
            'usd': ['USD', self.USD_RATE],
            'eur': ['Euro', self.EURO_RATE]
        }

        limit_rate = (abs(self.limit - self.get_today_stats()))
        currency_name = currency_info[currency][0]
        currency_rate = currency_info[currency][1]
        remains = round(limit_rate / currency_rate, 2)

        if self.counter_today < self.limit:
            return f'На сегодня осталось {remains} {currency_name}'
        elif self.counter_today == self.limit:
            return f"{'Денег нет, держись'}"
        else:
            return f'Денег нет, держись: твой долг - {remains} {currency_name}'
