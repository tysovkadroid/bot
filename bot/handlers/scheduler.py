from datetime import datetime, timedelta

from telegram.error import TelegramError
from telegram.utils.helpers import mention_markdown

from bot.config import LOGGER, TIMEZONE, DEFAULT_TIMESETTING, TYSOVKA_ID, DEFAULT_MARKUP, \
                       CREATOR_MARKUP, CREATOR_ID
from bot.msgs import msg_2, msg_10, msg_14
from bot.msgs.emojis import greeting_emoji, birthday_emoji
from bot.sql.get import get_users, get_table, get_birthday, get_verified, get_switched, \
                        get_prompted, get_ignored, get_holidays
from bot.sql.update import update_user, update_people, update_years, update_holidays
from bot.tools.list_join import list_join
from bot.tools.time_passed import time_passed
from bot.tools.word_form import word_form


def mention_layout(user_id, dsr_lst):
    users_rows = get_users()
    birthday_rows = get_birthday(TIMEZONE, user_id)
    mentions, line, declension = [], None, None
    if users_rows and birthday_rows:
        mention_lst = []
        for row in birthday_rows:
            userid = row[0]
            if userid in dsr_lst:
                username = row[1]
                mention = mention_markdown(userid, username, version=2)
                mention_lst.append(mention)
                update_years(user_id, userid)
        if len(birthday_rows) == 1:
            gender = birthday_rows[0][2]
            declension = word_form('его', gender)
            line = 'празднует свой день рождения'
        else:
            declension = 'их'
            line = 'празднуют свои дни рождения'
        mentions = list_join(mention_lst)
    return mentions, line, declension


def group_msgs(context):
    bot = context.bot
    now = datetime.now(TIMEZONE)
    if now.strftime('%H:%M') == DEFAULT_TIMESETTING:
        holiday_rows = get_holidays()
        if holiday_rows:
            data, latest = holiday_rows
            for date, txt in list(data.items()):
                date_today = now.strftime('%d.%m')
                current_year = int(now.strftime('%Y'))
                datetime_date = datetime(current_year, int(date[-2:]),
                                         int(date[:2]))
                datetime_shifted = datetime_date + timedelta(days=1)
                date_shifted = datetime_shifted.strftime('%d.%m')
                if date_today == date:
                    try:
                        bot_msg = bot.send_message(TYSOVKA_ID, txt)
                        bot_msg_id = bot_msg['message_id']
                        update_holidays('latest', bot_msg_id)
                        bot.pin_chat_message(TYSOVKA_ID, bot_msg_id)
                    except (Exception, TelegramError) as error:
                        LOGGER.info(error)
                elif date_today == date_shifted:
                    try:
                        bot.unpin_chat_message(TYSOVKA_ID, latest)
                    except (Exception, TelegramError) as error:
                        LOGGER.info(error)
        else:
            return None
    else:
        return None


def scheduler(context):
    group_msgs(context)
    users_rows = get_users()
    if users_rows:
        for row in users_rows:
            user_id = row[0]
            username = row[1]
            substate = row[7]
            if substate:
                bot = context.bot
                latest = row[11]
                if get_table(user_id):
                    now = datetime.now(TIMEZONE)
                    age_subquery = f"date_part('years', age(current_date, " \
                                   f"(SELECT birthday FROM users WHERE userid = {user_id})))"
                    birthdays = get_birthday(TIMEZONE, user_id)
                    if birthdays:
                        timesetting = row[8]
                        birthday_lst = [x[0] for x in birthdays]
                        ignored_lst = get_ignored(user_id)
                        refined_lst = list(set(birthday_lst) - set(ignored_lst))
                        if now.strftime('%H:%M') == timesetting and refined_lst:
                            switched_lst = get_switched(user_id, True)
                            prompted_lst = get_prompted(user_id)
                            crossed_lst = list(set(switched_lst) & set(prompted_lst))
                            repeated_lst = list(set(refined_lst) & set(prompted_lst))
                            update_user('age', age_subquery, user_id)
                            mentions, line, declension = mention_layout(user_id, birthday_lst)
                            greeting = msg_2.format(a=f', *{username}*', b=greeting_emoji()) + '\n'
                            msg = f"{greeting if time_passed(latest, '>=', 60) else ''}" + \
                                f"{'напоминаю, что ' if repeated_lst else ''}" + msg_10.format(
                                    a=mentions, b=line, c=declension, d=birthday_emoji())
                            bot.send_message(user_id, msg)
                            update_user('step', 'NULL', user_id)
                            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                            if crossed_lst:
                                for userid in crossed_lst:
                                    update_people(user_id, 'ignored', False, userid)
                    if now.strftime('%H:%M') == DEFAULT_TIMESETTING:
                        verified_lst = get_verified()
                        if verified_lst:
                            for userid in verified_lst:
                                update_user('age', age_subquery, userid)
                                update_people(user_id, 'ignored', False, userid)
                if time_passed(latest, '==', 5) and len(users_rows) > 1:
                    markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
                    if not get_table(user_id):
                        bot.send_message(user_id, msg_14, reply_markup=markup)
                    elif not get_switched(user_id, True):
                        bot.send_message(user_id, msg_14, reply_markup=markup)
    else:
        return None
