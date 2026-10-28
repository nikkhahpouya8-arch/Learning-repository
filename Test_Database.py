import sqlite3


connection = sqlite3.connect("TestBot.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY,
                   telegram_id INTEGER UNIQUE,
                   username TEXT,
                   city TEXT,
                   age INTEGER
               )
               """)


def add_user_info(telegram_id, username):

    user_info = get_user_info(telegram_id)

    print("Telegram ID:", telegram_id)
    print("Existing user:", user_info)

    if user_info is None:
        cursor.execute("""
                    INSERT INTO users(telegram_id, username)
                    VALUES(?,?)
                    """, (telegram_id, username))
        connection.commit()
    else:
        return



def add_user_city(telegram_id, city):

    print("ID recieved by add_user_city:", telegram_id)

    print("City recieved:", repr(city))

    cursor.execute("""
                SELECT * FROM users
                WHERE telegram_id = ?        
                """, (telegram_id,))
    print("Matching row before update:", cursor.fetchone())

    cursor.execute("""
                   UPDATE users
                   SET city = ?
                   WHERE telegram_id = ?
                   """, (city, telegram_id))

    print("Rows updated:", cursor.rowcount)

    cursor.execute("""
                SELECT city FROM users
                WHERE telegram_id = ?
                """, (telegram_id,))

    print("City stored:", repr(cursor.fetchone()["city"]))

    connection.commit()


def add_user_age(telegram_id, age):
    cursor.execute("""
                   UPDATE users
                   SET age = ?
                   WHERE telegram_id = ?
                   """, (age, telegram_id))
    connection.commit()


def get_user_info(telegram_id):
    cursor.execute("""
                       SELECT * FROM users
                       WHERE telegram_id = ?
                       """, (telegram_id,))

    return cursor.fetchone()
