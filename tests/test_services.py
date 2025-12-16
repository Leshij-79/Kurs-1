from unittest.mock import patch

from src.services import search_by_phone_number


@patch("src.services.read_operations_from_excel")
def test_search_by_phone_number(
    mock_search_by_phone_number, fixture_list_user_operations_two_days, fixture_search_by_phone_number
) -> None:
    """
    Тест поиска номера телефона в описании операции
    """
    mock_search_by_phone_number.return_value = fixture_list_user_operations_two_days
    result = search_by_phone_number()
    assert result == fixture_search_by_phone_number
