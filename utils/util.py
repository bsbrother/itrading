"""
  Utils for date and calendar operations

"""
import datetime
import re

DATE_PATTERN = re.compile(r"^([0-9]{4})[-/]?([0-9]{2})[-/]?([0-9]{2})")

# Chinese holidays (static list for major holidays, can be extended)
# Format: 'YYYYMMDD'
CHINESE_HOLIDAYS = {
    # 2024 holidays
    '20240101', '20240210', '20240211', '20240212', '20240213', '20240214', '20240215', '20240216', '20240217',  # New Year & Spring Festival
    '20240404', '20240405', '20240406',  # Qingming Festival
    '20240501', '20240502', '20240503',  # Labor Day
    '20240610',  # Dragon Boat Festival
    '20240915', '20240916', '20240917',  # Mid-Autumn Festival
    '20241001', '20241002', '20241003', '20241004', '20241005', '20241006', '20241007',  # National Day
    
    # 2025 holidays
    '20250101',  # New Year
    '20250128', '20250129', '20250130', '20250131', '20250201', '20250202', '20250203', '20250204',  # Spring Festival
    '20250404', '20250405', '20250406', '20250407',  # Qingming Festival
    '20250501', '20250502', '20250503',  # Labor Day
    '20250531',  # Dragon Boat Festival
    '20251006', '20251007', '20251008',  # Mid-Autumn Festival
    '20251001', '20251002', '20251003', '20251004', '20251005', '20251006', '20251007',  # National Day
    
    # 2026 holidays (can be extended)
    '20260101',  # New Year
    '20260216', '20260217', '20260218', '20260219', '20260220', '20260221', '20260222', '20260223',  # Spring Festival
}
def convert_trade_date(date: str | datetime.date | datetime.datetime) -> str:
    """
    Transform a date into a string representation trade_date format. e.g. 20160101

    :param date: 
        string e.g. 2016-01-01, 20160101 or 2016/01/01
        datetime.date or datetime.datetime
    :return: '20160101' or None
    """
    if isinstance(date, datetime.datetime) or isinstance(date, datetime.date):
        return date.strftime("%Y%m%d")
    elif isinstance(date, str):
        match = DATE_PATTERN.match(date)
        if match:
            groups = match.groups()
            if len(groups) == 3:
                try:
                    date_obj = datetime.date(
                        year=int(groups[0]), month=int(groups[1]), day=int(groups[2])
                    )
                    return date_obj.strftime("%Y%m%d")
                except ValueError:
                    return None
    return None

def last_trading_day(date: str | datetime.date | datetime.datetime) -> str:
    """
    Get last trading date from a given date for Chinese A-share market.

    :param date: 
        string e.g. 2016-01-01, 20160101 or 2016/01/01
        datetime.date or datetime.datetime
    :return: 'last_trade_date' or None
    """
    trade_date = convert_trade_date(date)
    if not trade_date:
        return None

    # Parse the date
    try:
        year = int(trade_date[:4])
        month = int(trade_date[4:6])
        day = int(trade_date[6:8])
        current_date = datetime.date(year, month, day)
    except ValueError:
        return None
    
    # If current date is a trading day, go back one day
    if is_trading_day(current_date):
        current_date -= datetime.timedelta(days=1)
    
    # Find the last trading day by going backwards
    max_days_back = 30  # Prevent infinite loop, max go back 30 days
    days_back = 0
    
    while days_back < max_days_back:
        if is_trading_day(current_date):
            return current_date.strftime("%Y%m%d")
        current_date -= datetime.timedelta(days=1)
        days_back += 1
    
    return None


def next_trading_day(date: str | datetime.date | datetime.datetime) -> str:
    """
    Get next trading date from a given date for Chinese A-share market.

    :param date: 
        string e.g. 2016-01-01, 20160101 or 2016/01/01
        datetime.date or datetime.datetime
    :return: 'next_trade_date' or None
    """
    trade_date = convert_trade_date(date)
    if not trade_date:
        return None

    # Parse the date
    try:
        year = int(trade_date[:4])
        month = int(trade_date[4:6])
        day = int(trade_date[6:8])
        current_date = datetime.date(year, month, day)
    except ValueError:
        return None
    
    # Start from the next day
    current_date += datetime.timedelta(days=1)
    
    # Find the next trading day by going forwards
    max_days_forward = 30  # Prevent infinite loop, max go forward 30 days
    days_forward = 0
    
    while days_forward < max_days_forward:
        if is_trading_day(current_date):
            return current_date.strftime("%Y%m%d")
        current_date += datetime.timedelta(days=1)
        days_forward += 1
    
    return None

def is_trading_day(date: str | datetime.date | datetime.datetime) -> bool:
    """
    Check if a given date is a trading day for Chinese A-share market.
    
    Chinese stock market rules:
    - Trading days: Monday to Friday
    - Market hours: 9:30-11:30, 13:00-15:00
    - Closed on weekends and Chinese public holidays

    :param date: 
        string e.g. 2016-01-01, 20160101 or 2016/01/01
        datetime.date or datetime.datetime
    :return: True if trading day, False otherwise
    """
    trade_date = convert_trade_date(date)
    if not trade_date:
        return False

    # Parse the date
    try:
        year = int(trade_date[:4])
        month = int(trade_date[4:6])
        day = int(trade_date[6:8])
        date_obj = datetime.date(year, month, day)
    except ValueError:
        return False
    
    # Check if it's a weekend (Saturday=5, Sunday=6)
    if date_obj.weekday() >= 5:
        return False
    
    # Check if it's a Chinese holiday
    if trade_date in CHINESE_HOLIDAYS:
        return False
    
    return True


if __name__ == "__main__":
    # Test convert_trade_date
    print("=== Testing convert_trade_date ===")
    d = datetime.datetime(2025, 7, 6, 17, 1, 0)  # Sunday
    print(f"convert_trade_date({d}) = {convert_trade_date(d)}")  # 20250706
    
    d = datetime.datetime.today()
    print(f"convert_trade_date(today) = {convert_trade_date(d)}")
    
    d = "2023-10-08"
    print(f"convert_trade_date('{d}') = {convert_trade_date(d)}")  # 20231008
    
    d = "2023/10/08"   
    print(f"convert_trade_date('{d}') = {convert_trade_date(d)}")  # 20231008
    
    d = "20231008"
    print(f"convert_trade_date('{d}') = {convert_trade_date(d)}")  # 20231008
    
    # Test is_trading_day
    print("\n=== Testing is_trading_day ===")
    test_dates = [
        "20250706",  # Sunday - should be False
        "20250707",  # Monday - should be True
        "20250101",  # New Year - should be False  
        "20250702",  # Wednesday - should be True
        "20241001",  # National Day - should be False
    ]
    
    for test_date in test_dates:
        result = is_trading_day(test_date)
        print(f"is_trading_day('{test_date}') = {result}")
    
    # Test last_trading_day
    print("\n=== Testing last_trading_day ===")
    test_dates = [
        "20250706",  # Sunday
        "20250707",  # Monday
        "20250101",  # New Year
    ]
    
    for test_date in test_dates:
        result = last_trading_day(test_date)
        print(f"last_trading_day('{test_date}') = {result}")
    
    # Test next_trading_day
    print("\n=== Testing next_trading_day ===")
    test_dates = [
        "20250704",  # Friday
        "20250705",  # Saturday  
        "20241231",  # Before New Year
    ]
    
    for test_date in test_dates:
        result = next_trading_day(test_date)
        print(f"next_trading_day('{test_date}') = {result}")
