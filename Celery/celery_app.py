from celery import Celery
import datetime

app = Celery("application_name", broker="redis://localhost:6379/0")


@app.task
def say_hello():
    return "Hello from celery!"


@app.task
def check_reminders():
    return "Checking database for due reminders..."


app.conf.beat_schedule = {
    "check-every-30-seconds": {
        "task": "celery_app.check_reminders",
        "schedule": 30.0,
    },
}
