import json
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv


def user_greeting(str_time: str) -> str:
    int_hour = int(str_time[:2])
    if int_hour > 5 and int_hour < 12:
        return 'Доброе утро'
    elif int_hour > 11 and int_hour < 18:
        return 'Добрый день'
    elif int_hour > 17 and int_hour < 24:
        return 'Добрый вечер'
    else:
        return 'Доброй ночи'


def read_operations_from_excel(path: str) -> list:
    path_excel_file_operation = os.path.abspath(path)
    try:
        excel_data = pd.read_excel(path_excel_file_operation)
        # logger.info("Данные с xlsx-файла прочитаны")
        return excel_data.to_dict("records")
    except FileNotFoundError:
        # logger.critical("XLSX-файл не найден")
        return []


def read_user_settings_from_json(path: str) -> list:
    path_json_file = os.path.abspath(path)
    try:
        with open(path_json_file, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        # logger.critical("Файл json не найден")
        # logger.critical(file_name)
        # logger.critical(os.path.dirname(__file__))
        # logger.critical(path_json_file)
        return []

    if len(data) == 0 or type(data) is not dict:
        # logger.error("Нет данных или не верный формат данных")
        return []
    else:
        # logger.info("Получены данные по транзакциям из json-файла")
        return data


def selection_of_operations_for_analysis(data: list, date_now: str) -> list:
    selected_operations = []
    start_date = datetime.strptime('01' + date_now[2:], '%d.%m.%Y')
    end_date = datetime.strptime(date_now + ' 23:59:59', '%d.%m.%Y %H:%M:%S')

    for operation in data:
        select_date = datetime.strptime(operation['Дата операции'], '%d.%m.%Y %H:%M:%S')
        if (start_date <= select_date <= end_date) and operation['Статус'] == 'OK':
            selected_operations.append(operation)

    return selected_operations


def processing_operations_main(data: list) -> list:
    list_data = []
    for operation in data:
        if type(operation['Номер карты']) == float:
            operation['Номер карты'] = '_NaN_'
        if len(list_data) == 0 and int(operation['Сумма операции']) < 0:
            temp_dict = {}
            temp_dict['last_digits'] = operation['Номер карты']
            temp_dict['total_spent'] = operation['Сумма операции с округлением']
            temp_dict['cashback'] = operation['Бонусы (включая кэшбэк)']
            list_data.append(temp_dict)
        else:
            for item in list_data:
                cont_ = 0
                if item['last_digits'] == operation['Номер карты']:
                    item['total_spent'] += operation['Сумма операции с округлением']
                    item['cashback'] = operation['Бонусы (включая кэшбэк)']
                    cont_ += 1
                    break
            if cont_ == 0 and int(operation['Сумма операции']) < 0:
                temp_dict = {}
                temp_dict['last_digits'] = operation['Номер карты']
                temp_dict['total_spent'] = operation['Сумма операции с округлением']
                temp_dict['cashback'] = operation['Бонусы (включая кэшбэк)']
                list_data.append(temp_dict)
    return list_data


def processing_operations_main_top_five(data: list) -> list:
    df = pd.DataFrame(data)
    sort_list = df.sort_values('Сумма операции с округлением', ascending=False)[:5]
    return sort_list.to_dict("records")


def exchange_rates(currencies: list = ["USD", "EUR"]) -> float | None:
    load_dotenv()
    api_key = os.getenv("API_KEY_EXCHANGE_RATES")
    base_ = "RUB"
    symbols_ = ','.join(currencies)
    url = (f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols_}&base={base_}")
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)

    status_code = response.status_code
    if status_code == 200:
        result = response.json()
    else:
        return {}

    for keys, values in result['rates'].items():
        result['rates'][keys] = round(1 / values, 2)

    return result


def stock_prices(stocks: list = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]) -> float | None:
    load_dotenv()
    api_key = os.getenv("API_KEY_STOCK_PRICES")
    symbol_ = ','.join(stocks)
    url = (f"https://api.twelvedata.com/price?symbol={symbol_}&apikey={api_key}")
    response = requests.get(url)

    status_code = response.status_code
    if status_code == 200:
        result = response.json()
    else:
        return {}

    return result
