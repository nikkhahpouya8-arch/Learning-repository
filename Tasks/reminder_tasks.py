from Celery.celery_app import app
from Services.reminder_services import get_reminders_to_notify
import datetime


@app.task
def check_reminders():

    current_time = datetime.datetime.now().astimezone()

    due_early_reminders, due_final_reminders = get_reminders_to_notify(
        current_time)

    for reminder in due_early_reminders:
        print(reminder["title"])

    for reminder in due_final_reminders:
        print(f"Reminder title: {reminder['title']}")
