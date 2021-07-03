from telegram import ForceReply

from bot.config import DEFAULT_MARKUP, END, CREATOR_ID, CREATOR_MARKUP, GENDER_MARKUP, \
                       USERNAME_STORED, GENDER_STORED, BIRTHDAY_STORED
from bot.msgs import msg_3, msg_5, msg_7, msg_15, msg_16
from bot.sql.get import get_user
from bot.sql.update import update_user
from bot.tools.chat_check import chat_check
from bot.tools.word_form import word_form


@chat_check('registered')
def sub_msg(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    db_user = get_user(user_id)
    username, gender, birthday, step = db_user[1], db_user[2], db_user[3], db_user[9]
    if not all([username, gender, birthday]):
        update_user('step', "'sub'", user_id)
        if not username:
            bot.send_message(user_id, msg_3, reply_markup=ForceReply())
            return USERNAME_STORED
        elif not gender:
            bot.send_message(user_id, msg_5, reply_markup=GENDER_MARKUP)
            return GENDER_STORED
        elif not birthday:
            bot.send_message(user_id, msg_7, reply_markup=ForceReply())
            return BIRTHDAY_STORED
    elif step == 'people':
        import bot.handlers.people as people
        people.people_msg(update, context)
    elif step == 'time':
        import bot.handlers.time as time
        time.time_msg(update, context)
    else:
        word = word_form('подписан', gender)
        update_user('substate', True, user_id)
        substate = db_user[7]
        if substate:
            msg = msg_16.format(a=word)
        else:
            verified, timesetting = db_user[6], db_user[8]
            if not verified:
                update_user('verified', True, user_id)
            msg = msg_15.format(a=word, b=timesetting)
        update_user('step', 'NULL', user_id)
        markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
        bot.send_message(user_id, msg, reply_markup=markup)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    return END
