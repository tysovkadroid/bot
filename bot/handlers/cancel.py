from datetime import datetime

from bot.config import DEFAULT_MARKUP, END, CREATOR_MARKUP, CREATOR_ID
from bot.msgs import msg_30, msg_31, msg_32, msg_33, msg_34
from bot.sql.get import get_user, get_verified, get_switched, get_prompted
from bot.sql.update import update_user, update_people
from bot.tools.chat_check import chat_check
from bot.tools.time_left import time_left


@chat_check('verified')
def cancel_msg(update, context):
    bot = context.bot
    user = update.effective_user
    user_id = user['id']
    db_user = get_user(user_id)
    timesetting, step = db_user[8], db_user[9]
    markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
    if step in ['people', 'time']:
        update_user('step', 'NULL', user_id)
        bot.send_message(user_id, msg_30, reply_markup=markup)
    elif step in ['on', 'off']:
        verified_lst = get_verified()
        switched_lst = get_switched(user_id, True)
        prompted_lst = get_prompted(user_id)
        crossed_lst = list(set(verified_lst) & set(prompted_lst))
        if prompted_lst:
            if switched_lst:
                update_user('step', 'NULL', user_id)
                if step == 'on':
                    if crossed_lst:
                        for userid in crossed_lst:
                            update_people(user_id, 'ignored', True, userid)
                    bot.send_message(user_id, msg_32, reply_markup=markup)
                else:
                    now = datetime.now()
                    timesetting_time = time_left(
                        now.replace(second=now.second+1, microsecond=0),
                        now.replace(hour=int(timesetting[:2]), minute=int(timesetting[-2:]),
                                    second=0, microsecond=0))
                    if crossed_lst and timesetting_time:
                        for userid in crossed_lst:
                            update_people(user_id, 'ignored', False, userid)
                        msg = msg_31.format(a=timesetting_time)
                        bot.send_message(user_id, msg, reply_markup=markup)
                    else:
                        bot.send_message(user_id, msg_30, reply_markup=markup)
            else:
                update_user('step', 'NULL', user_id)
                bot.send_message(user_id, msg_33, reply_markup=markup)
        else:
            update_user('step', 'NULL', user_id)
            bot.send_message(user_id, msg_34, reply_markup=markup)
    elif step in ['settings', 'holidays']:
        update_user('step', 'NULL', user_id)
        bot.send_message(user_id, msg_30, reply_markup=markup)
    else:
        update_user('step', 'NULL', user_id)
        bot.send_message(user_id, msg_34, reply_markup=markup)
    update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    return END
