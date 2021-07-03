from bot.sql import query_execute


def insert_user(userid):
    query = """
            INSERT INTO users (userid)
            VALUES ({0})
            ON CONFLICT (userid)
            DO NOTHING
            RETURNING userid;
            """
    out = query_execute(query.format(userid))
    return out[0] if out else 0


def insert_holiday(column, value):
    query = """
            INSERT INTO holidays ({0})
            VALUES ({1})
            RETURNING {0};
            """
    out = query_execute(query.format(column, value))
    return out[0] if out else 0
