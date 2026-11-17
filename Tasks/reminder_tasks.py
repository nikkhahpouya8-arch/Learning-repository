from Celery.celery_app import app
from Services.reminder_services import get_reminders_to_notify
from API.telegram_API import send_telegram_message
from Test_Database import get_telegram_id, mark_early_notice_sent, mark_final_notice_sent, get_reminder_by_id
import datetime
import asyncio


@app.task
def check_reminders():

    current_time = datetime.datetime.now().astimezone()

    due_early_reminders, due_final_reminders = get_reminders_to_notify(
        current_time)

    for reminder in due_early_reminders:
        message = f"{reminder['title']}"

        user_telegram_id = get_telegram_id(reminder['user_id'])

        if user_telegram_id is not None:
            asyncio.run(send_telegram_message(user_telegram_id, message))
            mark_early_notice_sent(reminder['id'])
        else:
            continue

    for reminder in due_final_reminders:
        message2 = f"Reminder title: {reminder['title']}"

        user_telegram_id2 = get_telegram_id(reminder['user_id'])

        if user_telegram_id2 is not None:
            asyncio.run(send_telegram_message(user_telegram_id2, message2))
            mark_final_notice_sent(reminder['id'])
        else:
            continue


@app.task
def send_early_notification(reminder_id):

    reminder = get_reminder_by_id(reminder_id)

    if reminder is None:
        return "Task not found!"

    notification = f"It's time!\n\nReminder title: {reminder['title']}"

    telegram_id = get_telegram_id(reminder['user_id'])

    if telegram_id is not None:
        asyncio.run(send_telegram_message(telegram_id, notification))
        mark_early_notice_sent(reminder['id'])
    else:
        return "User not found!"

@app.task
def send_final_notification(reminder_id):

    reminder = get_reminder_by_id(reminder_id)

    if reminder is None:
        return "Task not found!"

    notification = f"It's time!\n\nReminder title: {reminder['title']}"

    telegram_id = get_telegram_id(reminder['user_id'])

    if telegram_id is not None:
        asyncio.run(send_telegram_message(telegram_id, notification))
        mark_final_notice_sent(reminder['id'])
    else:
        return "User not found!"
