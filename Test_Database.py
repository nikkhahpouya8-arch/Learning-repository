import sqlite3


connection = sqlite3.connect("TestBot.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY,
                   telegram_id INTEGER,
                   username TEXT,
                   city TEXT,
                   age INTEGER
               )
               """)


def add_user_info(telegram_id, username):

    cursor.execute("""
                   INSERT INTO users(telegram_id, username)
                   VALUES(?,?)
                   """, (telegram_id, username))
    connection.commit()


def add_user_city(telegram_id, city):
    cursor.execute("""
                   UPDATE users
                   SET city = ?
                   WHERE telegram_id = ?
                   """, (telegram_id, city))
    connection.commit()


def add_user_age(telegram_id, age):
    cursor.execute("""
                   UPDATE users
                   SET age = ?
                   WHERE telegram_id = ?
                   """, (telegram_id, age))
    connection.commit()


def get_user_info(telegram_id):
    cursor.execute("""
                       SELECT * FROM users
                       WHERE telegram_id = ?
                       """, (telegram_id,))

    return cursor.fetchone()
