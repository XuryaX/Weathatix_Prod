from django.shortcuts import render

# Create your views here.

from django.views.generic import View,TemplateView
from models import WeatherStation,Subscriber
from django.http.response import HttpResponse
import datetime,json

class WeatherView(TemplateView):
    """ View which would have Weather Data  """
    template_name = "weather_views/index.html"

    def get_context_data(self, **kwargs):
        context = super(WeatherView, self).get_context_data(**kwargs)
        context["station_list"] = {}
        weather_stations = WeatherStation.objects.all()
        for station in weather_stations:
            context["station_list"].update({station.neighborhood:station.id})

        context["start"] = datetime.date.today().strftime("%Y-%m-%d")
        context["end"] = (datetime.date.today() + datetime.timedelta(days=9)).strftime("%Y-%m-%d")
        return context



class CreateStation(View):
    def put(self,request):
        body_unicode = request.body.decode('utf-8')
        req_json = json.loads(body_unicode)

        station_id = req_json['station_id']
        area = req_json['area']

        station_exists = WeatherStation.objects.filter(id=station_id)
        if len(station_exists):
            return HttpResponse("Registered")

        weather_station = WeatherStation(id=station_id,neighborhood=area)
        weather_station.save()

        return HttpResponse("Success!")


class Subscribe(View):
    def put(self,request):
        body_unicode = request.body.decode('utf-8')
        req_json = json.loads(body_unicode)
        station_id = req_json['station_id']
        weather_station = WeatherStation.objects.get(id=station_id)

        subscriber_exists = Subscriber.objects.filter(user=request.user,station_id=station_id)
        if len(subscriber_exists):
            return HttpResponse("Registered")

        new_subscriber = Subscriber(user=request.user,station=weather_station)
        new_subscriber.save()

        return HttpResponse("Success!")



