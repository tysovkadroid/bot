from bot.config import CREATOR_ID, TYSOVKA_ID
from bot.sql.get import get_user


def chat_check(method=None):
    def func_wrapper(func):
        def check_wrapper(update, context, *args, **kwargs):
            chat = update.effective_chat
            chat_type = chat['type']
            chat_id = chat['id']
            user = update.effective_user
            user_id = user['id']
            query = update.callback_query
            db_user = get_user(user_id)
            if method == 'exists':
                if not db_user:
                    if query:
                        query.answer()
                    return None
            elif method in ['registered', 'verified']:
                if db_user:
                    if method == 'registered' and not db_user[5]:
                        if query:
                            query.answer()
                        return None
                    elif method == 'verified' and not db_user[6]:
                        if query:
                            query.answer()
                        return None
                else:
                    if query:
                        query.answer()
                    return None
            elif method == 'tysovka':
                if not (chat_type == 'supergroup' and chat_id == TYSOVKA_ID):
                    if query:
                        query.answer()
                    return None
            elif method == 'creator':
                if not (chat_type == 'private' and chat_id == CREATOR_ID):
                    if query:
                        query.answer()
                    return None
            else:
                if query:
                    query.answer()
                return None
            return func(update, context, *args, **kwargs)
        return check_wrapper
    return func_wrapper
