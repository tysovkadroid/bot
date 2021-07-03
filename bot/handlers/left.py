from telegram.utils.helpers import mention_markdown

from bot.config import CREATOR_ID
from bot.handlers.people import people_refresh
from bot.msgs import msg_35
from bot.sql.delete import delete_user
from bot.sql.get import get_every, get_users, get_user
from bot.tools.chat_check import chat_check


@chat_check('tysovka')
def left_msg(update, context):
    message = update.message
    left_user = message.left_chat_member
    if not left_user.is_bot and left_user.id != CREATOR_ID:
        userid = str(left_user.id)
        every_rows = get_every()
        every_lst = [str(row[0]) for row in every_rows]
        if userid in every_lst:
            users_rows = get_users()
            users_lst = [str(row[0]) for row in users_rows]
            if userid in users_lst:
                username = get_user(userid)[1]
                mention = mention_markdown(userid, username, version=2)
                delete_user(userid)
                message.reply_text(msg_35.format(a=', ' + mention))
                people_refresh(context)
            else:
                delete_user(userid)
                message.reply_text(msg_35.format(a=''))
        else:
            message.reply_text(msg_35.format(a=''))
    else:
        return 0
