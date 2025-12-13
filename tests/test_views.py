from datetime import datetime
from unittest.mock import patch, Mock
from src.views import home_page
from tests.conftest import fixture_home_page


@patch("src.views.stock_prices")
@patch("src.views.read_user_settings_from_json")
@patch("src.views.read_operations_from_excel")
@patch("src.views.exchange_rates")
def test_home_page(
        mock_stock_prices,
        mock_read_user_settings_from_json,
        mock_read_operations_from_excel,
        mock_exchange_rates,
        fixture_list_user_operations_two_days,
        fixture_exchange_rates_now,
        fixture_stock_prices_now,
        fixture_home_page
) -> None:
    mock_user_settings = Mock()
    mock_user_settings.return_value = {
        'user_currencies': ['USD', 'EUR'],
        'user_stocks': ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']
    }
    mock_list_user_operations = Mock()
    mock_list_user_operations.some_method.side_effect = fixture_list_user_operations_two_days
    # mock_list_user_operations.return_value = fixture_list_user_operations_two_days
    mock_exchange_rates_now = Mock()
    mock_exchange_rates_now.some_method.side_effect = fixture_exchange_rates_now
    # mock_exchange_rates_now.return_value = fixture_exchange_rates_now
    mock_stock_prices_now = Mock()
    mock_stock_prices_now.some_method.side_effect = fixture_stock_prices_now
    # mock_stock_prices_now.return_value = fixture_stock_prices_now
    mock_read_user_settings_from_json.return_value = mock_user_settings
    mock_read_operations_from_excel.some_method.side_effect = mock_list_user_operations
    # mock_read_operations_from_excel.return_value = mock_list_user_operations
    mock_exchange_rates.return_value = mock_exchange_rates_now
    mock_stock_prices.return_value = mock_stock_prices_now
    assert home_page(datetime.now()) == fixture_home_page



