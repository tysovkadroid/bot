from telegram.utils.helpers import mention_markdown

from bot.config import CREATOR_ID, CREATOR_USERNAME
from bot.msgs import msg_1, msg_2, msg_35
from bot.msgs.emojis import emoji_5, emoji_9, greeting_emoji
from bot.sql.get import get_every, get_users, get_user
from bot.sql.insert import insert_user
from bot.tools.chat_check import chat_check
from bot.tools.version_get import version_get


@chat_check('tysovka')
def new_msg(update, context):
    bot = context.bot
    chat = update.effective_chat
    chat_id = chat['id']
    message = update.message
    new_user = message.new_chat_members[0]
    if not new_user.is_bot and new_user.id != CREATOR_ID:
        userid = str(new_user.id)
        every_rows = get_every()
        every_lst = [str(row[0]) for row in every_rows]
        if userid in every_lst:
            users_rows = get_users()
            users_lst = [str(row[0]) for row in users_rows]
            if userid in users_lst:
                username = get_user(userid)[1]
                mention = mention_markdown(userid, username, version=2)
                message.reply_text(msg_35.format(a=', ' + mention, b=greeting_emoji()))
            else:
                message.reply_text(msg_35.format(a='', b=greeting_emoji()))
        else:
            insert_user(userid)
            message.reply_text(msg_35.format(a='', b=greeting_emoji()))
    elif new_user.id == bot.id:
        greeting = msg_2.format(a=', *тусовка*', b=emoji_5)
        version = version_get()
        introduction = greeting + '\n' + msg_1.format(
            a='', b='вам', c='ваших', d=CREATOR_USERNAME,
            e=f'\nверсия {version} {emoji_9}' if version else '')
        bot.send_message(chat_id, introduction)
    else:
        return 0
