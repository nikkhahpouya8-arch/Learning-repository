from Test_Database import (
    add_reminder,
    update_reminder_task_ids,
    delete_failed_reminder,
    get_user_reminders,
    get_reminder_by_id,
    delete_reminder,
    edit_reminder
)
from Tasks.reminder_tasks import send_early_notification, send_final_notification
from Celery.celery_app import app
import datetime
from zoneinfo import ZoneInfo


def schedule_reminder(user_id, title, description, reminder_time):

    reminder_id = None

    if reminder_time > datetime.datetime.now():

        reminder_id = add_reminder(
            user_id, title, description, reminder_time)

        result = schedule_notifications(reminder_id, reminder_time)

        if result == "Failed":

            if reminder_id is not None:

                delete_failed_reminder(reminder_id)

            return "Failed"
        else:

            return result
    else:
        return "Past time"


def schedule_notifications(reminder_id, reminder_time):

    early_task_id = None

    try:

        early_time = reminder_time - datetime.timedelta(minutes=30)

        if reminder_time > datetime.datetime.now():
            if early_time >= datetime.datetime.now():
                early_task_id = send_early_notification.apply_async(
                    args=[reminder_id],
                    eta=early_time.replace(tzinfo=ZoneInfo("Asia/Tehran"))
                ).id
            else:
                early_task_id = None

            tehran_time = reminder_time.replace(
                tzinfo=ZoneInfo("Asia/Tehran")
            )

            final_task_id = send_final_notification.apply_async(
                args=[reminder_id],
                eta=tehran_time
            ).id

            update_reminder_task_ids(reminder_id, early_task_id, final_task_id)

            return "All done"
        else:
            return "Past time"

    except Exception as error:

        print(f"Scheduling failed: {error}")

        if early_task_id is not None:
            app.control.revoke(early_task_id)

        return "Failed"


def get_reminders(user_id):

    reminders = get_user_reminders(user_id)

    return reminders


def remove_reminder(reminder_id, user_id):

    reminder = get_reminder_by_id(reminder_id)

    if reminder is not None:

        if reminder["user_id"] == user_id:

            early_task_id = reminder["early_task_id"]

            final_task_id = reminder["final_task_id"]

            if early_task_id is not None:

                app.control.revoke(early_task_id)

            if final_task_id is not None:

                app.control.revoke(final_task_id)

            result = delete_reminder(reminder_id, user_id)

            if result == 1:

                return "Delete complete."

            elif result == 0:

                return "Delete failed."

            else:

                return "Unexpected error."

        else:

            return "Reminder doesn't belong to this user."
    else:
        return "Reminder not found."


def update_user_reminder(reminder_id, user_id, title, description, reminder_time):

    reminder = get_reminder_by_id(reminder_id)

    if reminder_time > datetime.datetime.now():

        if reminder is not None:
            if reminder['user_id'] == user_id:

                early_task_id = reminder['early_task_id']

                final_task_id = reminder['final_task_id']

                edit_reminder(reminder_id, user_id, title,
                              description, reminder_time)

                if early_task_id is not None:

                    app.control.revoke(early_task_id)

                if final_task_id is not None:

                    app.control.revoke(final_task_id)

                result = schedule_notifications(reminder_id, reminder_time)

                if result == "All done":

                    return "success"

                elif result == "Failed":

                    return "Failed"

            else:

                return "Reminder doesn't belong to this user."
        else:

            return "Reminder not found."

    else:

        return "Past time"
