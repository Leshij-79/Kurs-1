from datetime import datetime

from src.services import search_by_phone_number
from src.views import home_page

if __name__ == '__main__':
    print(home_page(datetime.now()))
    print('=' * 30)
    print(search_by_phone_number())