import json
import logging
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv


path_log_directory = os.path.join(os.path.dirname(__file__), "../logs", "utils.log")
logger = logging.getLogger(__name__) if __name__ != "__main__" else logging.getLogger("src.utils")
file_handler = logging.FileHandler(path_log_directory, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def user_greeting(str_time: str) -> str:
    """
    Функция формирования приветствия по времени суток
    :param str_time: Текущее время в формате строки
    :return: Сформированное приветствие
    """
    int_hour = int(str_time[:2])
    logger.info('Формирование приветствия')
    if int_hour > 5 and int_hour < 12:
        return 'Доброе утро'
    elif int_hour > 11 and int_hour < 18:
        return 'Добрый день'
    elif int_hour > 17 and int_hour < 24:
        return 'Добрый вечер'
    else:
        return 'Доброй ночи'


def read_operations_from_excel(path: str) -> list | None:
    """
    Функция чтения операций пользователя из xlsx-файла
    :param path: Путь к xlsx-файлу
    :return: Операции пользователя в формате списка
    """
    path_excel_file_operation = os.path.join(os.path.dirname(__file__), path)
    try:
        excel_data = pd.read_excel(path_excel_file_operation)
        logger.info("Данные с xlsx-файла прочитаны")
        return excel_data.to_dict("records")
    except FileNotFoundError:
        logger.critical("XLSX-файл не найден")
        logger.critical(os.path.dirname(__file__))
        return []
    except TypeError:
        logger.critical("Имя файла отсутствует")
        logger.critical(os.path.dirname(__file__))
        return []


def read_user_settings_from_json(path: str) -> dict | None:
    """
    Функция чтения настроек пользователя
    :param path: Путь к файлу настроек пользователя
    :return: Настройки пользователя в формате словаря
    """
    path_json_file = os.path.abspath(path)
    try:
        with open(path_json_file, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            logger.info("Данные с json-файла прочитаны")
    except FileNotFoundError:
        logger.critical("Файл json не найден")
        logger.critical(os.path.dirname(__file__))
        logger.critical(path_json_file)
        return []
    except PermissionError:
        logger.critical("Файл json не задан")
        logger.critical(os.path.dirname(__file__))
        logger.critical(path_json_file)
        return []

    if len(data) == 0 or type(data) is not dict:
        logger.error("Нет данных или не верный формат данных")
        return []
    else:
        logger.info("Получены данные по транзакциям из json-файла")
        return data


def selection_of_operations_for_analysis(data: list, date_now: str) -> list:
    """
    Функция отбора операций для анализа и группировки
    :param data: Операции пользователя в формате списка
    :param date_now: Текущая или необходимая дата в формате строки
    :return: Отобранные операции с формате списка
    """
    selected_operations = []
    start_date = datetime.strptime('01' + date_now[2:], '%d.%m.%Y')
    end_date = datetime.strptime(date_now + ' 23:59:59', '%d.%m.%Y %H:%M:%S')
    logger.info('Отбор операций начат')
    for operation in data:
        select_date = datetime.strptime(operation['Дата операции'], '%d.%m.%Y %H:%M:%S')
        if (start_date <= select_date <= end_date) and operation['Статус'] == 'OK':
            selected_operations.append(operation)
    logger.info('Отбор операций завершен')
    return selected_operations


def processing_operations_main(data: list) -> list:
    """
    Функция группировки операций по номерам карт
    :param data: Отобранные операции пользователя для группировки
    :return: Сгруппированные операции пользоватля в формате списка
    """
    list_data = []
    logger.info('Группировка операций начата')
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
    logger.info('Группировка операций завершена')
    return list_data


def processing_operations_main_top_five(data: list) -> list | None:
    """
    Функция отбора ТОП-5 операций пользователя за выбранный период
    :param data: Отобранные для анализа операции пользователя в ормате списка
    :return: Отобранные ТОП-5 операций пользователя в формате списка
    """
    logger.info('Отбор топ 5 операций начат')
    if len(data) == 0 or type(data) is not list:
        return []
    df = pd.DataFrame(data)
    sort_list = df.sort_values('Сумма операции с округлением', ascending=False)[:5]
    list_top_five_transactions = sort_list.to_dict("records")
    logger.info('Отбор топ 5 операций завершен')
    temp_list = []
    for item in list_top_five_transactions:
        temp_dict = {}
        temp_dict['date'] = item['Дата платежа']
        temp_dict['amount'] = item['Сумма операции с округлением']
        temp_dict['category'] = item['Категория']
        temp_dict['description'] = item['Описание']
        temp_list.append(temp_dict)
    logger.info('Преобразование данных завершено')
    return temp_list


def exchange_rates(currencies: list = ["USD", "EUR"]) -> list | None:
    """
    Функция запроса котировок валют на текущее время
    :param currencies: Список валют, по которым отправляется запрос на котировки в формате списка
    :return: Котировки валют в формате списка
    """
    logger.info('Запрос котировок валют начат')
    load_dotenv()
    api_key = os.getenv("API_KEY_EXCHANGE_RATES")
    base_ = "RUB"
    symbols_ = ','.join(currencies)
    url = (f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols_}&base={base_}")
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)
    logger.info('Получена реакция на запрос')
    status_code = response.status_code
    if status_code == 200:
        result = response.json()
        logger.info('Ответ на запрос сформирован')
    else:
        logger.error(f'Ошибка запроса - {status_code}. Ответ на запрос не сформирован. Возращен пустой список')
        return []
    for keys, values in result['rates'].items():
        result['rates'][keys] = round(1 / values, 2)
    logger.info('Котировки приведены в соответствие')
    temp_list = []
    for keys, values in result['rates'].items():
        temp_dict = {}
        temp_dict['currency'] = keys
        temp_dict['rate'] = values
        temp_list.append(temp_dict)
    logger.info('Преобразование данных завершено')
    return temp_list


def stock_prices(stocks: list = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]) -> list | None:
    """
    Функция запроса котировок акций
    :param stocks: Список акций, по которым делается запрос на котировки в формате списка
    :return: Котировки акций в формате списка
    """
    logger.info('Запрос котировок акций начат')
    load_dotenv()
    api_key = os.getenv("API_KEY_STOCK_PRICES")
    symbol_ = ','.join(stocks)
    url = (f"https://api.twelvedata.com/price?symbol={symbol_}&apikey={api_key}")
    response = requests.get(url)
    logger.info('Получена реакция на запрос')
    status_code = response.status_code
    if status_code == 200:
        result = response.json()
        logger.info('Ответ на запрос сформирован')
    else:
        logger.error(f'Ошибка запроса - {status_code}. Ответ на запрос не сформирован. Возращен пустой список')
        return []

    temp_list = []
    for keys, values in result.items():
        temp_dict = {}
        temp_dict['stock'] = keys
        temp_dict['price'] = values['price']
        temp_list.append(temp_dict)
    logger.info('Преобразование данных завершено')
    return temp_list
