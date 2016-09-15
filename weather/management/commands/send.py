from django.core.management.base import  BaseCommand

from weather.models import Subscriber,WeatherStation
from django.core.mail import EmailMessage
from weatherapi.common import get_api_data
from weatherapi.constants import CURRENT_OBS_URL
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        subscribers = Subscriber.objects.all()
        for subscriber in subscribers:
            email = subscriber.user.email
            station_id = subscriber.station.id
            area = subscriber.station.neighborhood

            url = CURRENT_OBS_URL+station_id+".json"
            self.stdout.write(url)
            temperature_details = json.loads(get_api_data(url))

            celsius = temperature_details["current_observation"]["temp_c"]
            fahrenheit = temperature_details["current_observation"]["temp_f"]

            msg = "Current Temperature : Celsius: "+str(celsius)+" Fahrenheit: "+str(fahrenheit)

            email = EmailMessage('Your Weather Update For '+area, msg, to=[email])
            email.send()

