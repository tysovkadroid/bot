from bot.sql import query_execute


def create_users():
    query = """
            CREATE TABLE IF NOT EXISTS users (
                userid      INTEGER               PRIMARY KEY UNIQUE NOT NULL,
                username    CHARACTER VARYING(32) DEFAULT NULL,
                gender      CHARACTER VARYING(6)  DEFAULT NULL,
                birthday    DATE                  DEFAULT NULL,
                age         CHARACTER VARYING(3)  DEFAULT NULL,
                registered  TIMESTAMPTZ           DEFAULT NULL,
                verified    BOOLEAN               DEFAULT FALSE,
                substate    BOOLEAN               DEFAULT FALSE,
                timesetting CHARACTER VARYING(5)  DEFAULT '00:00',
                step        CHARACTER VARYING(11) DEFAULT NULL,
                page        CHARACTER VARYING(10) DEFAULT NULL,
                latest      TIMESTAMPTZ           DEFAULT NULL
            );
            """
    query_execute(query, method='update')
