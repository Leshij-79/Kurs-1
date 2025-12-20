from datetime import datetime

import pandas as pd

from src.reports import spending_by_category
from src.services import search_by_phone_number
from src.utils import read_operations_from_excel
from src.views import home_page

if __name__ == "__main__":
    print(home_page(datetime.now()))
    print("=" * 30)
    print(search_by_phone_number())
    print("=" * 30)
    category = "Мобильная связь"
    date_now = "02.11.2021"
    print(
        spending_by_category(pd.DataFrame(read_operations_from_excel("../data/operations.xlsx")), category, date_now)
    )
