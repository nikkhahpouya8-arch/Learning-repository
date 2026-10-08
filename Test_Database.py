import sqlite3


connection = sqlite3.connect("TestBot.db")

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


def add_user_info(telegram_id, username, city, age):

    cursor.execute("""
                   INSERT INTO users(telegram_id, username, city, age)
                   VALUES(?,?,?,?)
                   """, (telegram_id, username, city, age))
    connection.commit()
