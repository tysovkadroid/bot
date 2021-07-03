from datetime import datetime

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import MAX_ANSWER_CALLBACK_QUERY_TEXT_LENGTH
from telegram.error import TelegramError

from bot.config import LOGGER, DEFAULT_MARKUP, END, CREATOR_ID, CREATOR_MARKUP
from bot.msgs import msg_11, msg_12, msg_13, msg_26, msg_27, msg_28
from bot.sql.get import get_users, get_user, get_table, get_people, get_verified, get_switched
from bot.sql.update import update_user, update_switchstate, update_global_switchstate
from bot.tools.chat_check import chat_check
from bot.tools.date_convert import date_convert
from bot.tools.list_join import list_join
from bot.tools.list_sort import list_sort
from bot.tools.time_left import time_left
from bot.tools.word_form import word_form


def people_birthdays(user_id):
    users_rows = get_users()
    closest, msgs = {}, {}
    for row in users_rows:
        userid = row[0]
        if userid != user_id:
            db_user = get_user(userid)
            username, gender, birthday = db_user[1], db_user[2], db_user[3]
            now = datetime.now()
            date_now = now.replace(hour=0, minute=0, second=0, microsecond=0)
            current_year = date_now.year
            date_today = date_now.strftime('%d.%m')
            birthday = datetime.min.replace(year=current_year, month=birthday.month,
                                            day=birthday.day)
            if date_today != birthday.strftime('%d.%m'):
                birthday_time = time_left(date_now, birthday)
                if birthday_time:
                    msg = msg_11.format(a=username, b='будет праздновать', c=birthday_time)
                else:
                    msg = msg_13.format(a=username, b=word_form('праздновал', gender))
                    birthday = birthday.replace(year=current_year + 1)
            else:
                msg = msg_12.format(a=username)
                birthday = birthday.replace(year=current_year + 1)
            closest.update({str(userid): [birthday, username]})
            msgs.update({str(userid): msg})
    return closest, msgs


def people_markup(user_id, page_type, page_num):
    people_rows = get_people(user_id)
    people, usernames = [], []
    for row in people_rows:
        userid = row[0]
        db_user = get_user(userid)
        verified = db_user[6]
        if verified:
            username = db_user[1]
            usernames.append(username)
            if page_type == 's':
                switchstate = row[1]
                toggle = 'включено' if switchstate else 'выключено'
                ppl_btns = [
                    InlineKeyboardButton(text=username, callback_data=f's_ttl_btn_{userid}'),
                    InlineKeyboardButton(text=toggle, callback_data=f's_tgl_btn_{userid}')
                ]
            else:
                birthday = db_user[3]
                birthday = date_convert(birthday)
                ppl_btns = [
                    InlineKeyboardButton(text=username, callback_data=f'd_ttl_btn_{userid}'),
                    InlineKeyboardButton(text=birthday, callback_data=f'd_tgl_btn_{userid}')
                ]
            people.append(ppl_btns)
    pages = list_sort(people, usernames)
    entries = [pages[x:x + 8] for x in range(0, len(pages), 8)][page_num]
    nav_btns = [InlineKeyboardButton(text='<', callback_data='p_btn'),
                InlineKeyboardButton(text='>', callback_data='n_btn')]
    if page_type == 's':
        switched_len = len(get_switched(user_id, True))
        non_switched_len = len(get_switched(user_id, False))
        mass_tgl = 'выключить всё' if switched_len >= non_switched_len else 'включить всё'
        g_btn = [InlineKeyboardButton(text=mass_tgl, callback_data='g_btn')]
        d_btn = [InlineKeyboardButton(text='даты', callback_data='d_btn')]
        controls = [g_btn, d_btn]
    else:
        c_btn = [InlineKeyboardButton(text='ближайший', callback_data='c_btn')]
        b_btn = [InlineKeyboardButton(text='назад', callback_data='b_btn')]
        controls = [c_btn, b_btn]
    if len(pages) > 8:
        entries.append(nav_btns)
    entries += controls
    markup = InlineKeyboardMarkup(entries)
    return markup


@chat_check('verified')
def people_msg(update, context):
    user = update.effective_user
    user_id = user['id']
    bot = context.bot
    substate = get_user(user_id)[7]
    markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
    if substate:
        update_user('step', 'NULL', user_id)
        update_user('page', "'s_0'", user_id)
        if get_people(user_id):
            bot.send_message(user_id, msg_27, reply_markup=people_markup(user_id, 's', 0))
        else:
            bot.send_message(user_id, msg_28, reply_markup=markup)
    else:
        update_user('step', "'people'", user_id)
        bot.send_message(user_id, msg_26, reply_markup=markup)
    update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
    return END


@chat_check('verified')
def people_cb(update, context):
    user = update.effective_user
    user_id = user['id']
    query = update.callback_query
    query_data = query['data']
    if get_verified():
        db_user = get_user(user_id)
        substate, page = db_user[7], db_user[10]
        page_type = page[:1]
        page_num = int(page[2:])
        if substate:
            update_user('step', 'NULL', user_id)
            if query_data[:9] in ['s_ttl_btn', 's_tgl_btn', 'd_ttl_btn', 'd_tgl_btn']:
                if query_data[:9] in ['s_ttl_btn', 's_tgl_btn']:
                    update_switchstate(user_id, query_data[10:])
                    query.edit_message_reply_markup(people_markup(user_id, 's', page_num))
                    update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                    query.answer()
                else:
                    msgs = people_birthdays(user_id)[1]
                    userid = query_data[10:]
                    msg = msgs[str(userid)]
                    update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                    query.answer(text=msg, show_alert=True)
            elif query_data in ['p_btn', 'n_btn']:
                pages_flt = len(get_verified()) / 8
                pages_int = int(pages_flt)
                pages_num = pages_int - 1 if pages_flt == pages_int else pages_int
                page_prv = page_num - 1 if page_num - 1 >= 0 else pages_num
                page_nxt = page_num + 1 if page_num + 1 <= pages_num else 0
                page_itr = page_prv if query_data == 'p_btn' else page_nxt
                update_user('page', f"'{page_type + '_' + str(page_itr)}'", user_id)
                query.edit_message_reply_markup(people_markup(user_id, page_type, page_itr))
                update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                query.answer()
            elif query_data == 'g_btn':
                switched_len = len(get_switched(user_id, True))
                non_switched_len = len(get_switched(user_id, False))
                global_switchstate = False if switched_len >= non_switched_len else True
                update_global_switchstate(user_id, global_switchstate)
                query.edit_message_reply_markup(people_markup(user_id, page_type, page_num))
                update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                query.answer()
            elif query_data == 'd_btn':
                update_user('page', f"'{'d_' + str(page_num)}'", user_id)
                query.edit_message_reply_markup(people_markup(user_id, 'd', page_num))
                update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                query.answer()
            elif query_data == 'c_btn':
                closest = people_birthdays(user_id)[0]
                if closest:
                    closest_items = list(closest.items())
                    closest_values = list(closest.values())
                    people_dates = [x[0] for x in closest_values]
                    now = datetime.now()
                    date_now = now.replace(hour=0, minute=0, second=0, microsecond=0)
                    birthday = min(people_dates, key=lambda x: abs(x - date_now))
                    closest_lst = []
                    for _, date in closest_items:
                        if date[0] == birthday:
                            closest_lst.append(date)
                    birthday_time = time_left(date_now, birthday)
                    line = 'будет' if len(closest_lst) == 1 else 'будут' + ' праздновать'
                    msg_len = len(msg_11.format(a='', b=line, c=birthday_time))
                    usernames = list_join(sorted([x[1] for x in closest_lst]),
                                          MAX_ANSWER_CALLBACK_QUERY_TEXT_LENGTH - msg_len)
                    msg = msg_11.format(a=usernames, b=line, c=birthday_time)
                    update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                    query.answer(text=msg, show_alert=True)
                else:
                    update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                    query.answer()
            elif query_data == 'b_btn':
                update_user('page', f"'{'s_' + str(page_num)}'", user_id)
                query.edit_message_reply_markup(people_markup(user_id, 's', page_num))
                update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
                query.answer()
            else:
                query.answer()
                return None
        else:
            update_user('step', "'people'", user_id)
            markup = CREATOR_MARKUP if user_id == CREATOR_ID else DEFAULT_MARKUP
            query.bot.send_message(user_id, msg_26, reply_markup=markup)
            update_user('latest', "'now()'::TIMESTAMPTZ", user_id)
            query.answer()
    else:
        query.edit_message_reply_markup(None)
        query.edit_message_text(msg_28)
    return END


def people_refresh(context):
    bot = context.bot
    users_rows = get_users()
    userid_lst = [str(row[0]) for row in users_rows]
    for userid in userid_lst:
        try:
            if get_table(userid):
                markup = people_markup(userid, 's', 0)
                bot.send_message(userid, msg_27, reply_markup=markup, disable_notification=True)
            else:
                markup = CREATOR_MARKUP if userid == CREATOR_ID else DEFAULT_MARKUP
                bot.send_message(userid, msg_28, reply_markup=markup, disable_notification=True)
        except (Exception, TelegramError) as error:
            LOGGER.info(error)
