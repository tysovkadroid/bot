from datetime import datetime

from telegram import ForceReply

from bot.config import GENDER_MARKUP, USERNAME_STORED, GENDER_STORED, BIRTHDAY_STORED, END
from bot.handlers.people import people_refresh
from bot.handlers.settings import settings_msg
from bot.handlers.sub import sub_msg
from bot.msgs import msg_3, msg_4, msg_5, msg_6, msg_7, msg_8, msg_9
from bot.sql.get import get_user
from bot.sql.update import update_user
from bot.tools.chat_check import chat_check
from bot.tools.datetime_check import datetime_check


@chat_check('registered')
def store_username(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    txt = update.message.text
    if txt.lower() in ['подписка', 'имя']:
        bot.send_message(user_id, msg_3, reply_markup=ForceReply())
        return USERNAME_STORED
    elif txt.lower() == 'пол':
        bot.send_message(user_id, msg_5, reply_markup=GENDER_MARKUP)
        return GENDER_STORED
    elif txt.lower() == 'дата рождения':
        bot.send_message(user_id, msg_7, reply_markup=ForceReply())
        return BIRTHDAY_STORED
    elif all([x.isalpha() for x in txt.split(' ')]):
        update_user('username', f"'{txt.title()}'", user_id)
        db_user = get_user(user_id)
        gender, birthday, step = db_user[2], db_user[3], db_user[9]
        if not gender:
            msg = msg_9.format(a=txt.lower()) + '\nтеперь ' + msg_5
            bot.send_message(user_id, msg, reply_markup=GENDER_MARKUP)
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return GENDER_STORED
        elif not birthday:
            msg = msg_9.format(a=txt) + '\nтеперь ' + msg_7
            bot.send_message(user_id, msg, reply_markup=ForceReply())
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return BIRTHDAY_STORED
        elif step == 'sub':
            sub_msg(update, context)
            people_refresh(context)
        elif step == 'settings':
            settings_msg(update, context)
            people_refresh(context)
        else:
            return None
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
    if txt.lower() == 'имя':
        bot.send_message(user_id, msg_3, reply_markup=ForceReply())
        return USERNAME_STORED
    elif txt.lower() in ['подписка', 'пол']:
        bot.send_message(user_id, msg_5, reply_markup=GENDER_MARKUP)
        return GENDER_STORED
    elif txt.lower() == 'дата рождения':
        bot.send_message(user_id, msg_7, reply_markup=ForceReply())
        return BIRTHDAY_STORED
    elif txt.lower() in ['мужской', 'женский']:
        gender = 'm' if txt.lower() == 'мужской' else 'f'
        update_user('gender', f"'{gender}'", user_id)
        db_user = get_user(user_id)
        username, birthday, step = db_user[1], db_user[3], db_user[9]
        if not username:
            msg = msg_9.format(a=txt.title()) + '\nтеперь ' + msg_3
            bot.send_message(user_id, msg, reply_markup=ForceReply())
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return USERNAME_STORED
        elif not birthday:
            msg = msg_9.format(a=txt) + '\nтеперь ' + msg_7
            bot.send_message(user_id, msg, reply_markup=ForceReply())
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return BIRTHDAY_STORED
        elif step == 'sub':
            sub_msg(update, context)
            people_refresh(context)
        elif step == 'settings':
            settings_msg(update, context)
            people_refresh(context)
        else:
            return None
    else:
        bot.send_message(user_id, msg_6, reply_markup=GENDER_MARKUP)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return GENDER_STORED
    return END


@chat_check('registered')
def store_birthday(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    txt = update.message.text
    if txt.lower() == 'имя':
        bot.send_message(user_id, msg_3, reply_markup=ForceReply())
        return USERNAME_STORED
    elif txt.lower() == 'пол':
        bot.send_message(user_id, msg_5, reply_markup=GENDER_MARKUP)
        return GENDER_STORED
    elif txt.lower() in ['подписка', 'дата рождения']:
        bot.send_message(user_id, msg_7, reply_markup=ForceReply())
        return BIRTHDAY_STORED
    elif datetime_check(txt, '%d.%m.%Y'):
        birthday_date = datetime.strptime(txt, '%d.%m.%Y')
        birthday = f"{birthday_date.strftime('%Y-%m-%d')}"
        update_user('birthday', f"'{birthday}'", user_id)
        msg = msg_9.format(a=txt)
        bot.send_message(user_id, msg)
        db_user = get_user(user_id)
        username, gender, step = db_user[1], db_user[2], db_user[9]
        if not username:
            msg = msg_9.format(a=txt.title()) + '\nтеперь ' + msg_3
            bot.send_message(user_id, msg, reply_markup=ForceReply())
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return USERNAME_STORED
        elif not gender:
            msg = msg_9.format(a=txt.lower()) + '\nтеперь ' + msg_5
            bot.send_message(user_id, msg, reply_markup=GENDER_MARKUP)
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            return GENDER_STORED
        elif step == 'sub':
            sub_msg(update, context)
            people_refresh(context)
        elif step == 'settings':
            settings_msg(update, context)
            people_refresh(context)
        else:
            return None
    else:
        bot.send_message(user_id, msg_8, reply_markup=ForceReply())
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return BIRTHDAY_STORED
    return END
