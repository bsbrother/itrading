"""
Test cases for utils/cons.py functions
"""
import datetime
import sys
import os

# Add the parent directory to the path so we can import from utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.cons import convert_trade_date, is_trading_day, last_trading_day, next_trading_day


def test_convert_trade_date():
    """Test convert_trade_date function"""
    print("=== Testing convert_trade_date ===")
    
    # Test datetime objects
    d1 = datetime.datetime(2025, 7, 6, 17, 1, 0)
    assert convert_trade_date(d1) == "20250706"
    
    d2 = datetime.date(2025, 1, 1)
    assert convert_trade_date(d2) == "20250101"
    
    # Test string formats
    assert convert_trade_date("2023-10-08") == "20231008"
    assert convert_trade_date("2023/10/08") == "20231008"  
    assert convert_trade_date("20231008") == "20231008"
    
    # Test invalid inputs
    assert convert_trade_date("invalid") is None
    assert convert_trade_date("") is None
    assert convert_trade_date("2023-13-01") is None  # Invalid month
    
    print("✓ convert_trade_date tests passed")


def test_is_trading_day():
    """Test is_trading_day function"""
    print("\n=== Testing is_trading_day ===")
    
    # Test weekdays (trading days)
    assert is_trading_day("20250707") == True  # Monday
    assert is_trading_day("20250708") == True  # Tuesday
    assert is_trading_day("20250709") == True  # Wednesday
    assert is_trading_day("20250710") == True  # Thursday
    assert is_trading_day("20250711") == True  # Friday
    
    # Test weekends (non-trading days)
    assert is_trading_day("20250705") == False  # Saturday
    assert is_trading_day("20250706") == False  # Sunday
    
    # Test Chinese holidays
    assert is_trading_day("20250101") == False  # New Year
    assert is_trading_day("20250128") == False  # Spring Festival
    assert is_trading_day("20250501") == False  # Labor Day
    assert is_trading_day("20241001") == False  # National Day
    
    # Test with different input formats
    assert is_trading_day(datetime.date(2025, 7, 7)) == True
    assert is_trading_day("2025-07-07") == True
    assert is_trading_day("2025/07/07") == True
    
    # Test invalid inputs
    assert is_trading_day("invalid") == False
    assert is_trading_day("") == False
    
    print("✓ is_trading_day tests passed")


def test_last_trading_day():
    """Test last_trading_day function"""
    print("\n=== Testing last_trading_day ===")
    
    # Test from Monday (should get previous Friday)
    assert last_trading_day("20250707") == "20250704"  # Monday -> Friday
    
    # Test from Sunday (should get previous Friday)
    assert last_trading_day("20250706") == "20250704"  # Sunday -> Friday
    
    # Test from Saturday (should get previous Friday)
    assert last_trading_day("20250705") == "20250704"  # Saturday -> Friday
    
    # Test around holidays
    result = last_trading_day("20250101")  # New Year
    assert result == "20241231"  # Should get Dec 31, 2024
    
    # Test from a trading day
    assert last_trading_day("20250702") == "20250701"  # Wednesday -> Tuesday
    
    # Test invalid inputs
    assert last_trading_day("invalid") is None
    assert last_trading_day("") is None
    
    print("✓ last_trading_day tests passed")


def test_next_trading_day():
    """Test next_trading_day function"""
    print("\n=== Testing next_trading_day ===")
    
    # Test from Friday (should get next Monday)
    assert next_trading_day("20250704") == "20250707"  # Friday -> Monday
    
    # Test from Saturday (should get next Monday)
    assert next_trading_day("20250705") == "20250707"  # Saturday -> Monday
    
    # Test from Sunday (should get next Monday)
    assert next_trading_day("20250706") == "20250707"  # Sunday -> Monday
    
    # Test around holidays
    result = next_trading_day("20241231")  # Dec 31, 2024 (before New Year)
    assert result == "20250102"  # Should get Jan 2, 2025 (skipping New Year)
    
    # Test from a trading day
    assert next_trading_day("20250701") == "20250702"  # Tuesday -> Wednesday
    
    # Test invalid inputs
    assert next_trading_day("invalid") is None
    assert next_trading_day("") is None
    
    print("✓ next_trading_day tests passed")


def test_edge_cases():
    """Test edge cases and special scenarios"""
    print("\n=== Testing edge cases ===")
    
    # Test around Spring Festival (multiple consecutive holidays)
    # Spring Festival 2025: Jan 28 - Feb 4
    assert is_trading_day("20250127") == True   # Day before Spring Festival
    assert is_trading_day("20250128") == False  # First day of Spring Festival
    assert is_trading_day("20250204") == False  # Last day of Spring Festival
    assert is_trading_day("20250205") == True   # Day after Spring Festival
    
    result = last_trading_day("20250130")  # During Spring Festival
    assert result == "20250127"  # Should go back to before festival
    
    result = next_trading_day("20250127")  # Day before Spring Festival
    assert result == "20250205"  # Should skip to after festival
    
    # Test around National Day (Oct 1-7)
    assert is_trading_day("20241001") == False  # National Day
    assert is_trading_day("20241007") == False  # Last day of National Day holiday
    assert is_trading_day("20241008") == True   # Day after National Day
    
    print("✓ Edge cases tests passed")


if __name__ == "__main__":
    test_convert_trade_date()
    test_is_trading_day()
    test_last_trading_day()
    test_next_trading_day()
    test_edge_cases()
    print("\n🎉 All tests passed!")
