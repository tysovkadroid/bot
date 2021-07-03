from datetime import datetime

from bot.tools.time_calculate import time_calculate


def time_passed(given, operator, minutes):
    if given:
        pattern = '%Y-%m-%d %H:%M:%S'
        given_time = datetime.strftime(given, pattern)
        given_diff = time_calculate(given_time, datetime.now().strftime(pattern), pattern)
        given_minutes = round(given_diff / 60)
        if operator == '==':
            return 1 if given_minutes == minutes else 0
        elif operator == '>=':
            return 1 if given_minutes >= minutes else 0
        elif operator == '<=':
            return 1 if given_minutes <= minutes else 0
        elif operator == '>':
            return 1 if given_minutes > minutes else 0
        elif operator == '<':
            return 1 if given_minutes < minutes else 0
        elif operator == '!=':
            return 1 if given_minutes != minutes else 0
        else:
            return None
    else:
        return None
