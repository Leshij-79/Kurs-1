import json
import logging
import os
from datetime import datetime

from src.utils import user_greeting, read_operations_from_excel, selection_of_operations_for_analysis, \
    processing_operations_main_top_five, processing_operations_main, exchange_rates, stock_prices, \
    read_user_settings_from_json


path_log_directory = os.path.join(os.path.dirname(__file__), "../logs", "views.log")
logger = logging.getLogger(__name__) if __name__ != "__main__" else logging.getLogger("src.views")
file_handler = logging.FileHandler(path_log_directory, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def home_page(datetime_now: datetime) -> list[dict]:
    """
    Функция главной страницы
    :param datetime_now: Необходимая дата и время в формате datetime
    :return: Сформированные данные в формате json-строки
    """
    time_now = datetime.strftime(datetime_now, "%H:%M:%S")
    date_now = datetime.strftime(datetime_now, "%d.%m.%Y")
    user_settings_read = 1
    time_now = '17:34:45' #  На время написания функционала
    date_now = '02.11.2021' #  На время написания функционала
    logger.info('Установлены дата и время')
    user_settings = read_user_settings_from_json('../user_settings.json')
    if user_settings == list():
        user_settings_read = 0
    logger.info('Прочитан файл настроек пользователя')
    greeting = user_greeting(time_now)
    logger.info('Сформировано приветствие')
    list_user_operations = read_operations_from_excel('../data/operations.xlsx')
    logger.info('Прочитаны операции пользователя')
    list_user_operations_per_month = selection_of_operations_for_analysis(list_user_operations, date_now)
    logger.info('Отбор операций за месяц произведен')
    list_sum_operations = processing_operations_main(list_user_operations_per_month)
    logger.info('Операции по картам сгруппированы')
    list_top_five_transactions = processing_operations_main_top_five(list_user_operations_per_month)
    logger.info('Отбор операций топ 5 произведен')
    if user_settings_read == 1:
        exchange_rates_now = exchange_rates(user_settings['user_currencies'])
        logger.info('Котеровки валют прочитаны')
        stock_prices_now = stock_prices(user_settings['user_stocks'])
        logger.info('Котировки акций прочитаны')
    else:
        exchange_rates_now = exchange_rates()
        logger.info('Котеровки валют прочитаны')
        stock_prices_now = stock_prices()
        logger.info('Котировки акций прочитаны')
    json_answer = {}
    json_answer['greeting'] = greeting
    json_answer['cards'] = list_sum_operations
    json_answer['top_transactions'] = list_top_five_transactions
    json_answer['currency_rates'] = exchange_rates_now
    json_answer['stock_prices'] = stock_prices_now
    logger.info('Сформирован json-ответ для главной страницы')
    return json.dumps(json_answer, ensure_ascii=False)
