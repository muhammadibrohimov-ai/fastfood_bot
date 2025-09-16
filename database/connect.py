import psycopg as sql

import sqlite3 as sql

from environs import Env
env = Env()
env.read_env()

# def get_connection():
#     return sql.connect(
#         dbname = env.str("DB_NAME"),
#         user = env.str("USERNAME_SQL"),
#         password = env.str("PASSWORD"),
#         host = env.str("HOST"),
#         port = env.str("PORT"),
#         autocommit=True
#     )

def get_connection():
    return sql.connect("fastfood.db",)

users = """
CREATE TABLE IF NOT EXISTS users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id  INTEGER UNIQUE,
    fullname VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL,
    phone    VARCHAR(100) UNIQUE,
    long     VARCHAR(50),
    lat      VARCHAR(50),
    is_admin INTEGER NOT NULL,
    UNIQUE(chat_id),
    UNIQUE(phone)
);

"""

foods = '''
CREATE TABLE IF NOT EXISTS foods (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(200),
    image       VARCHAR(250),
    price       INTEGER,
    quantity    INTEGER,
    description VARCHAR(500) NOT NULL DEFAULT 'This is food'
);
'''

orders = '''
CREATE TABLE IF NOT EXISTS orders (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id    INTEGER NOT NULL,
    user_id    INTEGER NOT NULL,
    quantity   INTEGER NOT NULL,
    price      DECIMAL(12,2) NOT NULL,
    status     VARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES foods(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
'''

comments = '''
CREATE TABLE IF NOT EXISTS comments(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    comment    TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);'''


# for table in [users, foods, orders, comments]:
#     with get_connection() as db:
#         dbc = db.cursor()
#         dbc.execute(table)
#         db.commit() 
        
