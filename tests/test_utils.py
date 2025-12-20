import json
from unittest.mock import Mock, mock_open, patch

import pandas as pd
import pytest

from src.utils import (exchange_rates, processing_operations_main, processing_operations_main_top_five,
                       read_operations_from_excel, read_user_settings_from_json, selection_of_operations_for_analysis,
                       stock_prices, user_greeting)


@pytest.mark.parametrize("str_time, expected", [("17:34:45", "Добрый день")])
def test_user_greeting_day(str_time: str, expected: str) -> None:
    """
    Тест на формирование приветствия
    """
    assert user_greeting(str_time) == expected


@pytest.mark.parametrize("str_time, expected", [("07:34:45", "Доброе утро")])
def test_user_greeting_morning(str_time: str, expected: str) -> None:
    """
    Тест на формирование приветствия
    """
    assert user_greeting(str_time) == expected


@pytest.mark.parametrize("str_time, expected", [("21:34:45", "Добрый вечер")])
def test_user_greeting_evening(str_time: str, expected: str) -> None:
    """
    Тест на формирование приветствия
    """
    assert user_greeting(str_time) == expected


@pytest.mark.parametrize("str_time, expected", [("01:34:45", "Доброй ночи")])
def test_user_greeting_night(str_time: str, expected: str) -> None:
    """
    Тест на формирование приветствия
    """
    assert user_greeting(str_time) == expected


@patch("pandas.read_excel")
def test_read_operations_from_excel(mock_read_from_excel, fixture_list_user_operations_two_days) -> None:
    """
    Тест на чтение операций из файла excel
    """
    data_mock_for_test = fixture_list_user_operations_two_days
    mock_read_from_excel.return_value = pd.DataFrame(data_mock_for_test)
    result = read_operations_from_excel("")
    assert result == data_mock_for_test


def test_read_operations_from_excel_error_no_name() -> None:
    """
    Тестирование excel-файла при ошибочном имени
    """
    assert read_operations_from_excel("") == []


def test_read_operations_from_excel_error() -> None:
    """
    Тестирование excel-файла при ошибочном имени
    """
    assert read_operations_from_excel("1.xlsx") == []


def test_read_operations_from_excel_no_name_file() -> None:
    """
    Тест на ошибку при чтении операций из файла excel без указания имени файла
    """
    with pytest.raises(TypeError):
        read_operations_from_excel()


@patch("builtins.open", new_callable=mock_open)
def test_read_user_settings_from_json(mock_read_from_json, fixture_user_settings) -> None:
    """
    Тест на чтение настроек пользователя из json-файла
    """
    data_mock_for_test = fixture_user_settings
    mock_file = mock_read_from_json.return_value
    mock_file.read.return_value = json.dumps(data_mock_for_test)
    assert read_user_settings_from_json("") == data_mock_for_test


def test_read_user_settings_from_json_error_no_name() -> None:
    """
    Тест на чтение настроек пользователя из json-файла без указании имени файла
    """
    assert read_user_settings_from_json("") == []


def test_read_user_settings_from_json_error() -> None:
    """
    Тест на чтение настроек пользователя из json-файла с указанием ошибочного имени файла
    """
    assert read_user_settings_from_json("1.json") == []


@patch("builtins.open", new_callable=mock_open)
def test_read_user_settings_from_json_no_data(mock_read_from_json, fixture_user_settings) -> None:
    """
    Чтение настроек пользователя из пустого json-файла
    """
    data_mock_for_test = []
    mock_file = mock_read_from_json.return_value
    mock_file.read.return_value = json.dumps(data_mock_for_test)
    assert read_user_settings_from_json("") == data_mock_for_test


def test_selection_of_operations_for_analysis(
    fixture_list_user_operations_three_days, fixture_list_user_operations_two_days
) -> None:
    """
    Тест на отбор операций за последние три месяца
    """
    assert (
        selection_of_operations_for_analysis(fixture_list_user_operations_three_days, "02.11.2021")
        == fixture_list_user_operations_two_days
    )


def test_processing_operations_main(fixture_list_user_operations_two_days, fixture_list_sum_operations) -> None:
    """
    Тест на суммирование операций по картам пользователя
    """
    assert processing_operations_main(fixture_list_user_operations_two_days) == fixture_list_sum_operations


def test_processing_operations_main_top_five(
    fixture_list_user_operations_two_days, fixture_list_top_five_transactions
) -> None:
    """
    Тест на формирование ТОП-5 операций
    """
    assert (
        processing_operations_main_top_five(fixture_list_user_operations_two_days)
        == fixture_list_top_five_transactions
    )


def test_processing_operations_main_top_five_no_data() -> None:
    """
    Тест на формирование ТОП-5 операций при отсутствии данных
    """
    assert processing_operations_main_top_five([]) == []


@patch("requests.get")
def test_exchange_rates(mock_requests_get, fixture_exchange_rates_now) -> None:
    """
    Тест запроса котеровок валют
    """
    mock_requests = Mock()
    mock_requests.status_code = 200
    mock_requests.json.return_value = {
        "success": True,
        "timestamp": 1765635186,
        "base": "RUB",
        "date": "2025-12-13",
        "rates": {"USD": 0.012551, "EUR": 0.010686},
    }
    mock_requests_get.return_value = mock_requests
    test_data = ["USD", "EUR"]
    assert exchange_rates(test_data) == fixture_exchange_rates_now


@patch("requests.get")
def test_exchange_rates_error(mock_requests_get) -> None:
    """
    Тест на запрос котеровок валют при ошибке сервера
    """
    mock_requests = Mock()
    mock_requests.status_code = 522
    mock_requests_get.return_value = mock_requests
    test_data = ["USD", "EUR"]
    assert exchange_rates(test_data) == []


@patch("requests.get")
def test_stock_prices(mock_requests_get, fixture_stock_prices_now) -> None:
    """
    Тест на запрос катеровок акций
    """
    mock_requests = Mock()
    mock_requests.status_code = 200
    mock_requests.json.return_value = {
        "AAPL": {"price": "278.28000"},
        "AMZN": {"price": "226.19000"},
        "GOOGL": {"price": "309.29001"},
        "MSFT": {"price": "478.53000"},
        "TSLA": {"price": "458.95999"},
    }
    mock_requests_get.return_value = mock_requests
    test_data = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    assert stock_prices(test_data) == fixture_stock_prices_now


@patch("requests.get")
def test_stock_prices_error(mock_requests_get) -> None:
    """
    Тест на запрос катеровок акций при ошибке сервера
    """
    mock_requests = Mock()
    mock_requests.status_code = 522
    mock_requests_get.return_value = mock_requests
    test_data = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    assert stock_prices(test_data) == []
