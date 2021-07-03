from telegram import ForceReply
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import CHANGE_MARKUP, GENDER_MARKUP, USERNAME_STORED, GENDER_STORED, \
                       BIRTHDAY_STORED, SETTING_CHOSEN, END
from bot.msgs import msg_3, msg_5, msg_6, msg_7, msg_36
from bot.sql.get import get_user
from bot.sql.update import update_user
from bot.tools.chat_check import chat_check
from bot.tools.string_escape import string_escape


@chat_check('verified')
def settings_msg(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    db_user = get_user(user_id)
    username, gender, birthday = db_user[1], db_user[2], db_user[3]
    if all([username, gender, birthday]):
        update_user('step', 'NULL', user_id)
        gender = 'мужской' if gender == 'm' else 'женский'
        birthday = birthday.strftime('%d.%m.%Y')
        msg = f'настройки:\n' \
              f'имя — *{username}*\n' \
              f'пол — *{gender}*\n' \
              f'дата рождения — *{birthday}*'
        button = [[InlineKeyboardButton(text='изменить', callback_data='s_btn')]]
        markup = InlineKeyboardMarkup(button)
        bot.send_message(user_id, string_escape(msg, '.'), reply_markup=markup)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    elif not username:
        bot.send_message(user_id, msg_3, reply_markup=ForceReply())
        return USERNAME_STORED
    elif not gender:
        bot.send_message(user_id, msg_5, reply_markup=GENDER_MARKUP)
        return GENDER_STORED
    elif not birthday:
        bot.send_message(user_id, msg_7, reply_markup=ForceReply())
        return BIRTHDAY_STORED
    return END


@chat_check('verified')
def settings_cb(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    query = update.callback_query
    data = query['data']
    if data == 's_btn':
        update_user('step', "'settings'", user_id)
        bot.send_message(user_id, msg_36, reply_markup=CHANGE_MARKUP)
        query.answer()
        return SETTING_CHOSEN
    else:
        query.answer()
        return None


def choose_setting(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    txt = update.message.text
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
        settings_msg(update, context)
    elif txt.lower() == 'праздники':
        import bot.handlers.holidays as holidays
        holidays.holidays_msg(update, context)
    elif txt.lower() == 'отмена':
        import bot.handlers.cancel as cancel
        cancel.cancel_msg(update, context)
    elif txt.lower() == 'имя':
        bot.send_message(user_id, msg_3, reply_markup=ForceReply())
        return USERNAME_STORED
    elif txt.lower() == 'пол':
        bot.send_message(user_id, msg_5, reply_markup=GENDER_MARKUP)
        return GENDER_STORED
    elif txt.lower() == 'дата рождения':
        bot.send_message(user_id, msg_7, reply_markup=ForceReply())
        return BIRTHDAY_STORED
    else:
        bot.send_message(user_id, msg_6, reply_markup=CHANGE_MARKUP)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return SETTING_CHOSEN
    return END
