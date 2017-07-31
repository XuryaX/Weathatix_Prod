__author__ = 'shaur'

from celery.decorators import task

from weather.models import Subscriber,WeatherStation
from django.core.mail import EmailMessage
from weatherapi.common import get_api_data
from weatherapi.constants import CURRENT_OBS_URL
import json

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

@task(name="send_update")
def send_update(subscriber_id):
    subscriber = Subscriber.objects.filter(user=subscriber_id)[0]
    send_subscriber_email(subscriber)


@periodic_task(
    run_every=(crontab(minute='*/2')),
    name="send_hourly_update",
    ignore_result=True
)
def send_hourly_updates():
    subscribers = Subscriber.objects.all()
    for subscriber in subscribers:
        send_subscriber_email(subscriber)


def send_subscriber_email(subscriber):
    email = subscriber.user.email
    station_id = subscriber.station.id
    area = subscriber.station.neighborhood

    url = CURRENT_OBS_URL+station_id+".json"
    temperature_details = json.loads(get_api_data(url))

    celsius = temperature_details["current_observation"]["temp_c"]
    fahrenheit = temperature_details["current_observation"]["temp_f"]

    msg = "Current Temperature : Celsius: "+str(celsius)+" Fahrenheit: "+str(fahrenheit)

    email = EmailMessage('Your Weather Update For '+area, msg, to=[email])
    email.send()