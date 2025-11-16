import os
from datetime import datetime

import pandas as pd


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