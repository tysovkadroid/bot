from datetime import datetime

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

from bot.config import TIMEZONE, DEFAULT_MARKUP, OPTIONS_MARKUP, TIME_ENTERED, TIME_REPEATED, \
                       CREATOR_ID, CREATOR_MARKUP, END
from bot.handlers.scheduler import mention_layout
from bot.msgs import msg_7, msg_9, msg_20, msg_21, msg_22, msg_23, msg_24, msg_25, msg_26
from bot.msgs.emojis import emoji_10, emoji_13, emoji_21
from bot.sql.get import get_user, get_table, get_birthday, get_switched, get_prompted
from bot.sql.update import update_user, update_people
from bot.tools.chat_check import chat_check
from bot.tools.datetime_check import datetime_check
from bot.tools.time_emoji import time_emoji
from bot.tools.time_left import time_left


@chat_check('verified')
def time_msg(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    substate = get_user(user_id)[7]
    if substate:
        update_user('step', 'NULL', user_id)
        timesetting = get_user(user_id)[8]
        if timesetting == '00:00':
            timesetting_type = msg_22.format(a=timesetting)
        else:
            timesetting_type = msg_23.format(a=timesetting)
        clock_emoji = time_emoji(timesetting)
        msg = msg_24.format(a=timesetting_type, b=clock_emoji)
        button = [[InlineKeyboardButton(text='изменить время', callback_data='t_btn')]]
        markup = InlineKeyboardMarkup(button)
        bot.send_message(user_id, msg, reply_markup=markup)
    else:
        update_user('step', "'time'", user_id)
        markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
        bot.send_message(user_id, msg_21, reply_markup=markup)
    update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    return END


@chat_check('verified')
def time_cb(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    query = update.callback_query
    query_data = query['data']
    db_user = get_user(user_id)
    substate = db_user[7]
    if substate:
        if query_data == 't_btn':
            substate = get_user(user_id)[7]
            if substate:
                update_user('step', "'enter_time'", user_id)
                bot.send_message(user_id, msg_20, reply_markup=ForceReply())
                update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                query.answer()
                return TIME_ENTERED
            else:
                update_user('step', "'time'", user_id)
                markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
                bot.send_message(user_id, msg_21, reply_markup=markup)
                update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                query.answer()
        else:
            query.answer()
            return None
    else:
        query.answer()
    return END


@chat_check('verified')
def enter_time(update, context):
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
        time_msg(update, context)
    elif txt.lower() == 'настройки':
        import bot.handlers.settings as settings
        settings.settings_msg(update, context)
    elif txt.lower() == 'праздники':
        import bot.handlers.holidays as holidays
        holidays.holidays_msg(update, context)
    elif txt.lower() == 'отмена':
        import bot.handlers.cancel as cancel
        cancel.cancel_msg(update, context)
    elif datetime_check(txt, '%M:%S'):
        update_user('timesetting', f"'{txt.zfill(5) if len(txt) == 4 else txt}'", user_id)
        timesetting = get_user(user_id)[8]
        clock_emoji = time_emoji(timesetting)
        msg = msg_26.format(a=timesetting, b=clock_emoji)
        if get_table(user_id):
            switched_lst = get_switched(user_id, True)
            prompted_lst = get_prompted(user_id)
            crossed_lst = list(set(switched_lst) & set(prompted_lst))
            if switched_lst:
                now = datetime.now()
                timesetting_time = time_left(
                    now.replace(second=now.second+1, microsecond=0),
                    now.replace(hour=int(timesetting[:2]), minute=int(timesetting[-2:]),
                                second=0, microsecond=0))
                if get_birthday(TIMEZONE, user_id) and timesetting_time:
                    if crossed_lst:
                        update_user('step', "'repeat_time'", user_id)
                        for userid in crossed_lst:
                            update_people(user_id, 'ignored', True, userid)
                        mentions = mention_layout(user_id, crossed_lst)[0]
                        msg = msg_25.format(a=mentions, b=timesetting)
                        bot.send_message(user_id, msg, reply_markup=OPTIONS_MARKUP)
                        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                        return TIME_REPEATED
                    else:
                        msg += '\n' + f'ты получишь уведомление через *{timesetting_time}* ' \
                                      f'{emoji_13}'
            else:
                msg += '\n' + f'не забудь определить свой *список людей* {emoji_21}'
        else:
            msg += '\n' + f'не забудь определить свой *список людей* {emoji_21}'
        update_user('step', 'NULL', user_id)
        markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
        bot.send_message(user_id, msg, reply_markup=markup)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    else:
        bot.send_message(user_id, msg_9, reply_markup=ForceReply())
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return TIME_ENTERED
    return END


@chat_check('verified')
def repeat_time(update, context):
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
        time_msg(update, context)
    elif txt.lower() == 'настройки':
        import bot.handlers.settings as settings
        settings.settings_msg(update, context)
    elif txt.lower() == 'праздники':
        import bot.handlers.holidays as holidays
        holidays.holidays_msg(update, context)
    elif txt.lower() == 'отмена':
        import bot.handlers.cancel as cancel
        cancel.cancel_msg(update, context)
    elif txt.lower() in ['да', 'нет']:
        timesetting = get_user(user_id)[8]
        clock_emoji = time_emoji(timesetting)
        msg = msg_26.format(a=timesetting, b=clock_emoji)
        if get_table(user_id):
            switched_lst = get_switched(user_id, True)
            prompted_lst = get_prompted(user_id)
            crossed_lst = list(set(switched_lst) & set(prompted_lst))
            if switched_lst:
                now = datetime.now()
                timesetting_time = time_left(now.replace(second=now.second+1, microsecond=0),
                                             now.replace(hour=int(timesetting[:2]),
                                                         minute=int(timesetting[-2:]),
                                                         second=0, microsecond=0))
                if txt.lower() == 'да':
                    if crossed_lst and timesetting_time:
                        update_user('step', "'on'", user_id)
                        for userid in crossed_lst:
                            update_people(user_id, 'ignored', False, userid)
                        line = f'ты получишь уведомление через *{timesetting_time}* {emoji_13}'
                        msg += '\n' + line
                else:
                    if crossed_lst and timesetting_time:
                        update_user('step', "'off'", user_id)
                        for userid in crossed_lst:
                            update_people(user_id, 'ignored', True, userid)
                        line = f'сегодня больше напоминать не буду {emoji_10}'
                        msg += '\n' + line
            else:
                msg += '\n' + f'не забудь определить свой *список людей* {emoji_21}'
        else:
            msg += '\n' + f'не забудь определить свой *список людей* {emoji_21}'
        update_user('step', 'NULL', user_id)
        markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
        bot.send_message(user_id, msg, reply_markup=markup)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    else:
        bot.send_message(user_id, msg_7, reply_markup=OPTIONS_MARKUP)
        update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
        return TIME_REPEATED
    return END
