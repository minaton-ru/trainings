import json
import requests
from config import currencies


class ConverionException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(amount: str, quote: str, base: str):
        if quote == base:
            raise ConverionException(f"Невозможно перевести одинаковые валюты {base}.")

        try:
            quote_ticker = currencies[quote.lower()]
        except KeyError:
            raise ConverionException(f"Валюта {base} не найдена в списке.")

        try:
            base_ticker = currencies[base.lower()]
        except KeyError:
            raise ConverionException(f"Валюта {base} не найдена в списке.")

        try:
            amount = float(amount)
        except ValueError:
            raise ConverionException(f'Не удалось обработать количество {amount}.')

        request = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        resp = json.loads(request.content)

        if base_ticker == 'RUB':
            quote_value = resp['Valute'][quote_ticker]['Value']
            new_price = round(amount * quote_value, 2)
        elif quote_ticker == 'RUB':
            base_value = resp['Valute'][base_ticker]['Value']    
            new_price = round(amount / base_value, 2)
        else:
            base_value = resp['Valute'][base_ticker]['Value']
            quote_value = resp['Valute'][quote_ticker]['Value']
            new_price = round(amount * quote_value / base_value, 2)

        result = f"Цена {amount} {quote} в {base}: {new_price}"
        return result
