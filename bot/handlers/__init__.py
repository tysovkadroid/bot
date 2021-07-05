import re

from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler, \
                         ConversationHandler, Filters

from bot.config import LOGGER, CREATOR_ID, USERNAME_STORED, GENDER_STORED, BIRTHDAY_STORED, \
                       TIME_ENTERED, TIME_REPEATED, SETTING_CHOSEN, HOLIDAY_ADDED, END
from bot.handlers.cancel import cancel_msg
from bot.handlers.holidays import holidays_msg, holidays_cb, process_holiday
from bot.handlers.left import left_msg
from bot.handlers.new import new_msg
from bot.handlers.people import people_msg, people_cb
from bot.handlers.settings import settings_msg, choose_setting, settings_cb
from bot.handlers.start import start_cmd
from bot.handlers.store import store_username, store_gender, store_birthday
from bot.handlers.sub import sub_msg
from bot.handlers.time import time_msg, enter_time, repeat_time, time_cb
from bot.handlers.unsub import unsub_msg


def exit_conversation(update, context):
    return END


def error_cb(update, context):
    LOGGER.warning(context.error)


def register_handlers(dispatcher):
    start_command_handler = CommandHandler('start', start_cmd)
    sub_message_handler = MessageHandler(
        Filters.regex(re.compile(r'^подписка$', re.IGNORECASE)), sub_msg)
    unsub_message_handler = MessageHandler(
        Filters.regex(re.compile(r'^отписка$', re.IGNORECASE)), unsub_msg)
    people_message_handler = MessageHandler(
        Filters.regex(re.compile(r'^люди$', re.IGNORECASE)), people_msg)
    time_message_handler = MessageHandler(
        Filters.regex(re.compile(r'^время$', re.IGNORECASE)), time_msg)
    settings_message_handler = MessageHandler(
        Filters.regex(re.compile(r'^настройки$', re.IGNORECASE)), settings_msg)
    holidays_message_handler = MessageHandler(
        Filters.regex(re.compile(r'^праздники$', re.IGNORECASE)) &
        Filters.chat(CREATOR_ID), holidays_msg)
    cancel_message_handler = MessageHandler(
        Filters.regex(re.compile(r'^отмена$', re.IGNORECASE)), cancel_msg)
    new_message_handler = MessageHandler(Filters.status_update.new_chat_members, new_msg)
    left_message_handler = MessageHandler(Filters.status_update.left_chat_member, left_msg)
    time_cb_handler = CallbackQueryHandler(time_cb, pattern=r'^t_btn$')
    people_cb_handler = CallbackQueryHandler(people_cb, pattern=r'^s_ttl_btn_+\d*$|'
                                                                r'^s_tgl_btn_+\d*$|'
                                                                r'^d_ttl_btn_+\d*$|'
                                                                r'^d_tgl_btn_+\d*$|'
                                                                r'^p_btn$|^n_btn$|'
                                                                r'^g_btn$|^d_btn$|'
                                                                r'^c_btn$|^b_btn$')
    settings_cb_handler = CallbackQueryHandler(settings_cb, pattern=r'^s_btn$')
    holidays_cb_handler = CallbackQueryHandler(holidays_cb, pattern=r'^h_btn$')
    sub_conversation_handler = ConversationHandler(
        entry_points=[sub_message_handler],
        states={USERNAME_STORED: [MessageHandler(Filters.text, store_username)],
                GENDER_STORED: [MessageHandler(Filters.text, store_gender)],
                BIRTHDAY_STORED: [MessageHandler(Filters.text, store_birthday)]},
        fallbacks=[MessageHandler(Filters.text, exit_conversation)],
        allow_reentry=True,
        name='SubConversationHandler')
    time_conversation_handler = ConversationHandler(
        entry_points=[time_cb_handler],
        states={TIME_ENTERED: [MessageHandler(Filters.text, enter_time)],
                TIME_REPEATED: [MessageHandler(Filters.text, repeat_time)]},
        fallbacks=[MessageHandler(Filters.text, exit_conversation)],
        allow_reentry=True,
        name='TimeConversationHandler')
    settings_conversation_handler = ConversationHandler(
        entry_points=[settings_message_handler, settings_cb_handler],
        states={SETTING_CHOSEN: [MessageHandler(Filters.text, choose_setting)],
                USERNAME_STORED: [MessageHandler(Filters.text, store_username)],
                GENDER_STORED: [MessageHandler(Filters.text, store_gender)],
                BIRTHDAY_STORED: [MessageHandler(Filters.text, store_birthday)]},
        fallbacks=[MessageHandler(Filters.text, exit_conversation)],
        allow_reentry=True,
        name='SettingsConversationHandler')
    holidays_conversation_handler = ConversationHandler(
        entry_points=[holidays_message_handler, holidays_cb_handler],
        states={HOLIDAY_ADDED: [MessageHandler(Filters.text, process_holiday)]},
        fallbacks=[MessageHandler(Filters.text, exit_conversation)],
        allow_reentry=True,
        name='HolidayConversationHandler')
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(sub_conversation_handler)
    dispatcher.add_handler(unsub_message_handler)
    dispatcher.add_handler(time_message_handler)
    dispatcher.add_handler(time_conversation_handler)
    dispatcher.add_handler(people_message_handler)
    dispatcher.add_handler(people_cb_handler)
    dispatcher.add_handler(cancel_message_handler)
    dispatcher.add_handler(settings_conversation_handler)
    dispatcher.add_handler(holidays_conversation_handler)
    dispatcher.add_handler(new_message_handler)
    dispatcher.add_handler(left_message_handler)
    dispatcher.add_error_handler(error_cb)
