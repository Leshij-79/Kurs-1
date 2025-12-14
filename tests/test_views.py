import json
from datetime import datetime
from unittest.mock import patch, Mock
from src.views import home_page
from tests.conftest import fixture_home_page


@patch("src.views.stock_prices")
@patch("src.views.read_user_settings_from_json")
@patch("src.views.read_operations_from_excel")
@patch("src.views.exchange_rates")
def test_home_page(
        mock_exchange_rates,
        mock_read_operations_from_excel,
        mock_read_user_settings_from_json,
        mock_stock_prices,
        fixture_list_user_operations_two_days,
        fixture_exchange_rates_now,
        fixture_stock_prices_now,
        fixture_home_page,
        fixture_user_settings
) -> None:
    mock_stock_prices.return_value = fixture_stock_prices_now
    mock_read_user_settings_from_json.return_value = fixture_user_settings
    mock_read_operations_from_excel.return_value = fixture_list_user_operations_two_days
    mock_exchange_rates.return_value = fixture_exchange_rates_now
    result = home_page(datetime.now())
    assert result == json.dumps(fixture_home_page, ensure_ascii=False)

@patch("src.views.stock_prices")
@patch("src.views.read_user_settings_from_json")
@patch("src.views.read_operations_from_excel")
@patch("src.views.exchange_rates")
def test_home_page_no_user_settings(
        mock_exchange_rates,
        mock_read_operations_from_excel,
        mock_read_user_settings_from_json,
        mock_stock_prices,
        fixture_list_user_operations_two_days,
        fixture_exchange_rates_now,
        fixture_stock_prices_now,
        fixture_home_page,
        fixture_user_settings
) -> None:
    mock_stock_prices.return_value = fixture_stock_prices_now
    mock_read_user_settings_from_json.return_value = []
    mock_read_operations_from_excel.return_value = fixture_list_user_operations_two_days
    mock_exchange_rates.return_value = fixture_exchange_rates_now
    result = home_page(datetime.now())
    assert result == json.dumps(fixture_home_page, ensure_ascii=False)
