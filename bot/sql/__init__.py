import psycopg2

from psycopg2 import DatabaseError

from bot.config import LOGGER, DATABASE_URL

connection = psycopg2.connect(DATABASE_URL, sslmode='require')


def query_execute(query, method='fetch'):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        if query.split(' ', 1)[0] != 'SELECT':
            connection.commit()
        if method == 'fetch':
            out = cursor.fetchall()
            cursor.close()
            return out
        else:
            cursor.close()
    except (Exception, DatabaseError) as error:
        LOGGER.warning(error)
