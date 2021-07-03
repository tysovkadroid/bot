from datetime import datetime


def datetime_check(string, formatting):
    try:
        datetime.strptime(string, formatting)
        return True
    except (Exception, ValueError):
        return False
