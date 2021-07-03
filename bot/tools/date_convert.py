def date_convert(date):
    month = date.strftime('%m')
    day = date.strftime('%-d')
    if month == '01':
        date = day + ' января'
    elif month == '02':
        date = day + ' февраля'
    elif month == '03':
        date = day + ' марта'
    elif month == '04':
        date = day + ' апреля'
    elif month == '05':
        date = day + ' мая'
    elif month == '06':
        date = day + ' июня'
    elif month == '07':
        date = day + ' июля'
    elif month == '08':
        date = day + ' августа'
    elif month == '09':
        date = day + ' сентября'
    elif month == '10':
        date = day + ' октября'
    elif month == '11':
        date = day + ' ноября'
    elif month == '12':
        date = day + ' декабря'
    else:
        return None
    return date
