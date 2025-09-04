import psycopg as sql

from environs import Env
env = Env()
env.read_env()

def get_connection():
    return sql.connect(
        dbname = env.str("DB_NAME"),
        user = env.str("USERNAME_SQL"),
        password = env.str("PASSWORD"),
        host = env.str("HOST"),
        port = env.str("PORT"),
        autocommit=True
    )

