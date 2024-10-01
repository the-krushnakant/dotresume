from datetime import datetime

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%B %Y")
        return True
    except ValueError:
        return False
