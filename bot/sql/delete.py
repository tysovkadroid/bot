from bot.sql import query_execute


def delete_user(userid):
    query = """
            DROP TABLE IF EXISTS people_{0};
            DELETE FROM users
            WHERE userid = {0}
            RETURNING*;
            """
    out = query_execute(query.format(userid))
    return out if out else 0
