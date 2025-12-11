import json
from datetime import datetime

from src.utils import user_greeting, read_operations_from_excel, selection_of_operations_for_analysis, \
    processing_operations_main_top_five, processing_operations_main, exchange_rates, stock_prices, \
    read_user_settings_from_json


def home_page(datetime_now: datetime) -> list[dict]:
    time_now = datetime.strftime(datetime_now, "%H:%M:%S")
    date_now = datetime.strftime(datetime_now, "%d.%m.%Y")
    time_now = '17:34:45' #  На время написания функционала
    date_now = '16.11.2021' #  На время написания функционала

    user_settings = read_user_settings_from_json('../user_settings.json')

    greeting = user_greeting(time_now)
    list_user_operations = read_operations_from_excel('../data/operations.xlsx')
    list_user_operations_per_month = selection_of_operations_for_analysis(list_user_operations, date_now)
    list_sum_operations = processing_operations_main(list_user_operations_per_month)
    list_top_five_transactions = processing_operations_main_top_five(list_user_operations_per_month)
    exchange_rates_now = exchange_rates(user_settings['user_currencies'])
    stock_prices_now = stock_prices(user_settings['user_stocks'])
    json_answer = {}
    json_answer['greeting'] = greeting
    json_answer['cards'] = list_sum_operations

    temp_list = []
    for item in list_top_five_transactions:
        temp_dict = {}
        temp_dict['date'] = item['Дата платежа']
        temp_dict['amount'] = item['Сумма операции с округлением']
        temp_dict['category'] = item['Категория']
        temp_dict['description'] = item['Описание']
        temp_list.append(temp_dict)
    json_answer['top_transactions'] = temp_list

    temp_list = []
    for keys, values in exchange_rates_now['rates'].items():
        temp_dict = {}
        temp_dict['currency'] = keys
        temp_dict['rate'] = values
        temp_list.append(temp_dict)
    json_answer['currency_rates'] = temp_list

    temp_list = []
    for keys, values in stock_prices_now.items():
        temp_dict = {}
        temp_dict['stock'] = keys
        temp_dict['price'] = values['price']
        temp_list.append(temp_dict)
    json_answer['stock_prices'] = temp_list

    return json.dumps(json_answer, ensure_ascii=False)

if __name__ == '__main__':
    print(home_page(datetime.now()))
