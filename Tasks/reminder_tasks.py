from Celery.celery_app import app
from API.telegram_API import send_telegram_message
from Test_Database import get_telegram_id, mark_early_notice_sent, mark_final_notice_sent, get_reminder_by_id
import asyncio


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
