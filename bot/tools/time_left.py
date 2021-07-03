from dateutil import relativedelta

from bot.tools.word_form import word_form


def time_left(date_start, date_end):
    out, seconds = None, int((date_end-date_start).total_seconds())
    if seconds > 0:
        diff = relativedelta.relativedelta(date_end, date_start)
        years = diff.years
        if years != 0:
            out = f"{word_form('год', integer=years)}"
        else:
            months = diff.months
            days = diff.days
            if months != 0 or days != 0:
                if months != 0 and days == 0:
                    out = f"{word_form('месяц', integer=months)}"
                elif months == 0 and days != 0:
                    out = f"{word_form('день', integer=days)}"
                elif months != 0 and days != 0:
                    out = f"{word_form('месяц', integer=months)} и " \
                          f"{word_form('день', integer=days)}"
            else:
                hours = diff.hours
                minutes = diff.minutes
                seconds = diff.seconds
                if hours != 0 and minutes == 0 and seconds == 0:
                    out = f"{word_form('час', integer=hours)}"
                elif hours == 0 and minutes != 0 and seconds == 0:
                    out = f"{word_form('минуту', integer=minutes)}"
                elif hours == 0 and minutes == 0 and seconds != 0:
                    out = f"{word_form('секунду', integer=seconds)}"
                elif hours != 0 and minutes != 0 and seconds == 0:
                    out = f"{word_form('час', integer=hours)} и " \
                          f"{word_form('минуту', integer=minutes)}"
                elif hours != 0 and minutes == 0 and seconds != 0:
                    out = f"{word_form('час', integer=hours)} и " \
                          f"{word_form('секунду', integer=seconds)}"
                elif hours == 0 and minutes != 0 and seconds != 0:
                    out = f"{word_form('минуту', integer=minutes)} и " \
                          f"{word_form('секунду', integer=seconds)}"
                elif hours != 0 and minutes != 0 and seconds != 0:
                    out = f"{word_form('час', integer=hours)}, " \
                          f"{word_form('минуту', integer=minutes)} и " \
                          f"{word_form('секунду', integer=seconds)}"
    return out
