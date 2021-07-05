from datetime import datetime

from telegram import ForceReply

from bot.config import SUB_GENDER_MARKUP, SETTINGS_GENDER_MARKUP, USERNAME_STORED, \
                       GENDER_STORED, BIRTHDAY_STORED, END
from bot.handlers.people import people_refresh
from bot.handlers.settings import settings_msg
from bot.handlers.sub import sub_msg
from bot.msgs import msg_3, msg_4, msg_5, msg_6, msg_7, msg_8, msg_9, msg_10
from bot.sql.get import get_users, get_user
from bot.sql.update import update_user
from bot.tools.chat_check import chat_check
from bot.tools.datetime_check import datetime_check


@chat_check('registered')
def store_username(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    txt = update.message.text
    users_rows = get_users()
    username_lst = [row[1] for row in users_rows] if users_rows else []
    if txt in username_lst:
        bot.send_message(user_id, msg_5, reply_markup=ForceReply())
        return USERNAME_STORED
    elif all([x.isalpha() for x in txt.split(' ')]) and txt:
        update_user('username', f"'{txt.title()}'", user_id)
        db_user = get_user(user_id)
        gender, birthday, step = db_user[2], db_user[3], db_user[9]
        msg = msg_10.format(a=txt.title())
        if not gender:
            msg += '\n' + msg_6
            if step == 'sub':
                markup = SUB_GENDER_MARKUP
            elif step == 'settings':
                markup = SETTINGS_GENDER_MARKUP
            bot.send_message(user_id, msg, reply_markup=markup)
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return GENDER_STORED
        elif not birthday:
            msg += '\n' + msg_8
            bot.send_message(user_id, msg, reply_markup=ForceReply())
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return BIRTHDAY_STORED
        else:
            bot.send_message(user_id, msg, reply_markup=None)
            if step == 'sub':
                sub_msg(update, context)
            elif step == 'settings':
                settings_msg(update, context)
            # TODO: check whether works for both (sub, settings) cases
            people_refresh(context, user_id)
    else:
        bot.send_message(user_id, msg_4, reply_markup=ForceReply())
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return USERNAME_STORED
    return END


@chat_check('registered')
def store_gender(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    txt = update.message.text
    db_user = get_user(user_id)
    step = db_user[9]
    if txt.lower() in ['мужской', 'женский']:
        gender = 'm' if txt.lower() == 'мужской' else 'f'
        update_user('gender', f"'{gender}'", user_id)
        username, birthday = db_user[1], db_user[3]
        msg = msg_10.format(a=txt.lower())
        if not username:
            msg += '\n' + msg_3
            bot.send_message(user_id, msg, reply_markup=ForceReply())
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return USERNAME_STORED
        elif not birthday:
            msg += '\n' + msg_8
            bot.send_message(user_id, msg, reply_markup=ForceReply())
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return BIRTHDAY_STORED
        else:
            bot.send_message(user_id, msg, reply_markup=None)
            if step == 'sub':
                sub_msg(update, context)
            elif step == 'settings':
                settings_msg(update, context)
            # TODO: check whether works for both (sub, settings) cases
            people_refresh(context, user_id)
    else:
        if step == 'sub':
            markup = SUB_GENDER_MARKUP
        elif step == 'settings':
            markup = SETTINGS_GENDER_MARKUP
        bot.send_message(user_id, msg_7, reply_markup=markup)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return GENDER_STORED
    return END


@chat_check('registered')
def store_birthday(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    txt = update.message.text
    if datetime_check(txt, '%d.%m.%Y'):
        birthday_date = datetime.strptime(txt, '%d.%m.%Y')
        birthday = f"{birthday_date.strftime('%Y-%m-%d')}"
        update_user('birthday', f"'{birthday}'", user_id)
        db_user = get_user(user_id)
        username, gender, step = db_user[1], db_user[2], db_user[9]
        msg = msg_10.format(a=txt)
        if not username:
            msg += '\n' + msg_3
            bot.send_message(user_id, msg, reply_markup=ForceReply())
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return USERNAME_STORED
        elif not gender:
            msg += '\n' + msg_6
            if step == 'sub':
                markup = SUB_GENDER_MARKUP
            elif step == 'settings':
                markup = SETTINGS_GENDER_MARKUP
            bot.send_message(user_id, msg, reply_markup=markup)
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return GENDER_STORED
        else:
            bot.send_message(user_id, msg, reply_markup=None)
            if step == 'sub':
                sub_msg(update, context)
            elif step == 'settings':
                settings_msg(update, context)
            # TODO: check whether works for both (sub, settings) cases
            people_refresh(context, user_id)
    else:
        bot.send_message(user_id, msg_9, reply_markup=ForceReply())
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return BIRTHDAY_STORED
    return END
