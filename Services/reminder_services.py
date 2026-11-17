from Test_Database import get_due_early_reminders, get_due_final_reminders
from Tasks.reminder_tasks import send_early_notification


# def create_reminder_task():
#     result = send_early_notification.apply_async(
#         args=[reminder_id],
#         eta=early_time
#     )