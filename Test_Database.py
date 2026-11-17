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

cursor.execute("""
               CREATE TABLE IF NOT EXISTS reminders(
                   id INTEGER PRIMARY KEY,
                   user_id INTEGER NOT NULL,
                   title TEXT NOT NULL,
                   description TEXT,
                   reminder_time TEXT NOT NULL,
                   early_notice INTEGER NOT NULL DEFAULT 0,
                   final_notice INTEGER NOT NULL DEFAULT 0
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


def get_due_early_reminders(current_time):
    cursor.execute("""
                   SELECT * FROM reminders
                   WHERE reminder_time > ?
                   AND reminder_time <= datetime(?, '+30 minutes')
                   AND early_notice = 0
                   """, (current_time, current_time))
    return cursor.fetchall()


def get_due_final_reminders(current_time):
    cursor.execute("""
                   SELECT * FROM reminders
                   WHERE reminder_time <= ?
                   AND final_notice = 0
                   """, (current_time,))
    return cursor.fetchall()


def mark_early_notice_sent(reminder_id):
    cursor.execute("""
                   UPDATE reminders
                   SET early_notice = 1
                   WHERE id = ?
                   """, (reminder_id,))
    connection.commit()


def mark_final_notice_sent(reminder_id):
    cursor.execute("""
                    UPDATE reminders
                    SET final_notice = 1
                    WHERE id = ?
                    """, (reminder_id,))
    connection.commit()


def add_reminder(user_id, title, description, reminder_time):
    cursor.execute("""
                   INSERT INTO reminders(user_id, title, description, reminder_time)
                   VALUES(?,?,?,?)
                   """, (user_id, title, description, reminder_time))
    connection.commit()


def get_user_reminders(user_id):
    cursor.execute("""
                   SELECT * FROM reminders
                   WHERE user_id = ?
                   """, (user_id,))
    return cursor.fetchall()


def delete_reminder(reminder_id, user_id):
    cursor.execute("""
                   DELETE FROM reminders
                   WHERE id = ?
                   AND user_id = ?
                   """, (reminder_id, user_id))
    connection.commit()


def edit_reminder(reminder_id, user_id, title, description, reminder_time):
    cursor.execute("""
                   UPDATE reminders
                   SET title = ?,
                    description = ?,
                    reminder_time = ?
                   WHERE id = ?
                   AND user_id = ?
                   """, (title, description, reminder_time, reminder_id, user_id))
    connection.commit()

def get_telegram_id(user_id):
    cursor.execute("""
                   SELECT telegram_id FROM users
                   WHERE id = ?
                   """, (user_id,))
    row = cursor.fetchone()
    
    return row['telegram_id'] if row else None

def get_reminder_by_id(reminder_id):
    cursor.execute("""
                   SELECT * FROM reminders
                   WHERE id = ?
                   """, (reminder_id,))
    reminder = cursor.fetchone()
    
    return reminder