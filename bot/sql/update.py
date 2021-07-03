from bot.sql import query_execute


def update_user(column, value, user_id):
    query = """
            UPDATE users
            SET {0} = {1}
            WHERE userid = {2};
            """
    query_execute(query.format(column, value, user_id), method='update')


def update_people(user_id, column, value, userid):
    query = """
            UPDATE people_{0}
            SET {1} = {2}
            WHERE userid = {3};
            """
    query_execute(query.format(user_id, column, value, userid), method='update')


def update_switchstate(user_id, userid):
    query = """
            UPDATE people_{0}
                SET switchstate = CASE
                    WHEN switchstate = TRUE
                    THEN FALSE
                    WHEN switchstate = FALSE
                    THEN TRUE
                    ELSE FALSE
                END
            WHERE userid = {1};
            """
    query_execute(query.format(user_id, userid), method='update')


def update_global_switchstate(user_id, switchstate):
    query = """
            UPDATE people_{0}
            SET switchstate = {1}
            WHERE userid != {0};
            """
    query_execute(query.format(user_id, switchstate), method='update')


def update_years(user_id, userid):
    query = """
            UPDATE people_{0}
            SET years = array_append(years, date_part('year', CURRENT_DATE))
            WHERE date_part('year', CURRENT_DATE) != ANY(years)
            OR years is NULL
            AND userid = {1};
            """
    query_execute(query.format(user_id, userid), method='update')


def update_holidays(column, value):
    query = """
            UPDATE holidays
            SET {0} = {1};
            """
    query_execute(query.format(column, value), method='update')
