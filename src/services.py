import json
import logging
import os
import re

from src.utils import read_operations_from_excel


path_log_directory = os.path.join(os.path.dirname(__file__), "../logs", "services.log")
logger = logging.getLogger(__name__) if __name__ != "__main__" else logging.getLogger("src.services")
file_handler = logging.FileHandler(path_log_directory, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def search_by_phone_number() -> list[dict]:
    """
    Функция поиска транзакций, в описании которых есть номер телефона
    :return: Отобранные транзакции по запросу пользователя
    """
    list_user_operations = read_operations_from_excel('../data/operations.xlsx')
    logger.info('Прочитаны операции пользователя')
    json_answer = []
    for operation in list_user_operations:
        temp = re.search(r'\d\d\d-\d\d-\d\d', operation['Описание'])
        if temp is not None:
            json_answer.append(operation)
    logger.info('Операции отобраны')
    return json.dumps(json_answer, ensure_ascii=False)
