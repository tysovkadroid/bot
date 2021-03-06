from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import HOLIDAY_ADDED, END
from bot.msgs import msg_39, msg_38, msg_40, msg_41
from bot.sql.get import get_holidays
from bot.sql.insert import insert_holiday
from bot.sql.update import update_holidays
from bot.sql.update import update_user
from bot.tools.chat_check import chat_check
from bot.tools.datetime_check import datetime_check
from bot.tools.string_check import string_check
from bot.tools.string_escape import string_escape


def holidays_layout(data):
    holidays = []
    for date, txt in list(data.items()):
        chars = '[]()>#+-=|{}.!'
        date = string_escape(date, chars)
        txt = string_escape(txt, chars)
        holidays.append(f'{date} — {txt}')
    holidays = '\n'.join(holidays)
    out = f'праздники:\n{holidays}'
    return out


@chat_check('creator')
def holidays_msg(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    update_user('step', 'NULL', user_id)
    holidays_rows = get_holidays()
    if any(holidays_rows):
        msg = holidays_layout(holidays_rows[0])
    else:
        msg = msg_39
    button = [[InlineKeyboardButton(text='изменить', callback_data='h_btn')]]
    markup = InlineKeyboardMarkup(button)
    bot.send_message(user_id, msg, reply_markup=markup)
    update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    return END


@chat_check('creator')
def holidays_cb(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    query = update.callback_query
    data = query['data']
    if data == 'h_btn':
        update_user('step', "'holidays'", user_id)
        bot.send_message(user_id, msg_38)
        query.answer()
        return HOLIDAY_ADDED
    else:
        query.answer()
        return None


def process_holiday(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    txt = update.message.text
    holidays_rows = get_holidays()
    values = txt.split(', ', 1)
    button = [[InlineKeyboardButton(text='повторить попытку', callback_data='h_btn')]]
    markup = InlineKeyboardMarkup(button)
    if txt.lower() == '/start':
        import bot.handlers.start as start
        start.start_cmd(update, context)
    elif txt.lower() == 'подписка':
        import bot.handlers.sub as sub
        sub.sub_msg(update, context)
    elif txt.lower() == 'отписка':
        import bot.handlers.unsub as unsub
        unsub.unsub_msg(update, context)
    elif txt.lower() == 'люди':
        import bot.handlers.people as people
        people.people_msg(update, context)
    elif txt.lower() == 'время':
        import bot.handlers.time as time
        time.time_msg(update, context)
    elif txt.lower() == 'настройки':
        import bot.handlers.settings as settings
        settings.settings_msg(update, context)
    elif txt.lower() == 'праздники':
        holidays_msg(update, context)
    elif txt.lower() == 'отмена':
        import bot.handlers.cancel as cancel
        cancel.cancel_msg(update, context)
    elif len(values) == 2:
        if datetime_check(values[0], '%d.%m') and string_check(values[1], '*_~`'):
            date, text = values
            if get_holidays():
                data_subquery = f"""data || '{{"{date}":"{text}"}}'::jsonb"""
                update_holidays('data', data_subquery)
            else:
                data_subquery = f"""'{{"{date}":"{text}"}}'::jsonb"""
                inserted = insert_holiday('data', data_subquery)
                if not inserted:
                    bot.send_message(user_id, msg_41.format(a=''), reply_markup=markup)
                    return END
            holidays_msg(update, context)
        else:
            bot.send_message(user_id, msg_41.format(a=string_escape('!\nневерный формат', '!')),
                             reply_markup=markup)
    else:
        if datetime_check(txt, '%d.%m'):
            data = holidays_rows[0] if any(holidays_rows) else {}
            if txt in list(data.keys()):
                data_subquery = f"""data - '{txt}'"""
                update_holidays('data', data_subquery)
                holidays_msg(update, context)
            else:
                bot.send_message(user_id, msg_40.format(a=txt), reply_markup=markup)
        else:
            bot.send_message(user_id, msg_41.format(a=string_escape('!\nневерный формат', '!')),
                             reply_markup=markup)
    return END
