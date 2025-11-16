from datetime import datetime

from src.utils import user_greeting, read_operations_from_excel, selection_of_operations_for_analysis, \
    processing_operations_main_top_five, processing_operations_main


def home_page(datetime_now: datetime) -> list[dict]:
    time_now = datetime.strftime(datetime_now, "%H:%M:%S")
    date_now = datetime.strftime(datetime_now, "%d.%m.%Y")
    time_now = '17:34:45' #  На время написания функционала
    date_now = '16.11.2021' #  На время написания функционала

    greeting = user_greeting(time_now)
    list_user_operations = read_operations_from_excel('../data/operations.xlsx')
    list_user_operations_per_month = selection_of_operations_for_analysis(list_user_operations, date_now)
    list_sum_operations = processing_operations_main(list_user_operations_per_month)
    list_top_five_transactions = processing_operations_main_top_five(list_user_operations_per_month)


if __name__ == '__main__':
    home_page(datetime.now())
