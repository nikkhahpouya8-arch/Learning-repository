from celery import Celery
import datetime

app = Celery("application_name", broker="redis://localhost:6379/0")

app.conf.imports = ("Tasks.reminder_tasks",)

@app.task
def say_hello():
    return "Hello from celery!"


app.conf.beat_schedule = {
    "check-every-30-seconds": {
        "task": "Tasks.reminder_tasks.check_reminders",
        "schedule": 30.0,
    },
}
