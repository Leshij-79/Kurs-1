import logging
import os
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta


path_log_directory = os.path.join(os.path.dirname(__file__), "../logs", "reports.log")
logger = logging.getLogger(__name__) if __name__ != "__main__" else logging.getLogger("src.reports")
file_handler = logging.FileHandler(path_log_directory, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def json_file_writer(func):
    """
    Декоратор записи в json-файл
    """
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        path_file = os.path.join(os.path.dirname(__file__), "../data", "operations.json")
        result.to_json(path_file, force_ascii = False)
        logger.info('Запись в json-файл произведена')
        return result
    return wrapper


@json_file_writer
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Фунция подготовки отчёта по транзакциям в выбранной категории за три месяца от выбраной даты
    :param transactions: Транзакции пользователя в формате DataFrame
    :param category: Категория транзакций по которым необходим отбор
    :param date: Дата по которую необходим отбор
    :return: Отобранные транзакции по запросу пользователя
    """
    if date is None or date == '':
        date = datetime.strftime(datetime.now(), "%d.%m.%Y")
    end_date = datetime.strptime(date, '%d.%m.%Y')
    start_date = end_date - relativedelta(months=3)
    end_date = datetime.strptime(date + ' 23:59:59', '%d.%m.%Y %H:%M:%S')
    logger.info('Начальная и конечная дата установлены')
    filtered_category = transactions[transactions['Категория'] == category]
    filtered_days_start_date = filtered_category[start_date <= pd.to_datetime(filtered_category['Дата операции'],
                                                                              dayfirst=True,
                                                                              format = '%d.%m.%Y %H:%M:%S')]
    filtered_days = filtered_days_start_date[pd.to_datetime(filtered_days_start_date['Дата операции'],
                                                            dayfirst=True,
                                                            format = '%d.%m.%Y %H:%M:%S') <= end_date]
    logger.info('Отбор данных произведён')
    return filtered_days