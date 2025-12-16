from unittest.mock import patch

import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category(fixture_spending_by_category, fixture_list_user_operations_two_days):
    """
    Тест поиска по категории
    """
    category = 'Мобильная связь'
    date_now = '02.11.2021'
    start_data = pd.DataFrame(fixture_list_user_operations_two_days)
    result_data = fixture_spending_by_category
    assert spending_by_category(start_data, category, date_now).to_dict("records") == result_data


def test_spending_by_category_no_date(fixture_spending_by_category, fixture_list_user_operations_two_days):
    """
    Тест поиска по категории без указания даты
    """
    category = 'Мобильная связь'
    start_data = pd.DataFrame(fixture_list_user_operations_two_days)
    result_data = []
    assert spending_by_category(start_data, category).to_dict("records") == result_data

