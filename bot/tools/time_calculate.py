from datetime import datetime


def time_calculate(start, end, pattern):
    start_time = datetime.strptime(start, pattern)
    end_time = datetime.strptime(end, pattern)
    seconds = int((end_time - start_time).total_seconds())
    return seconds
