from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from common import get_api_data
from constants import API_URL
from django.http.response import HttpResponse
import json,os


class StationList(View):
    def get(self,request,country,city):
        url = API_URL +"/geolookup/q/"+country+"/"+city+".json"
        station_json = json.loads(get_api_data(url))

        json_response = json.dumps(station_json['location']
                                    ['nearby_weather_stations']
                                    ['pws'])
        return HttpResponse(json_response)


class HourlyForecast(View):
    def get(self,request,station,epochstart,epochend):
        url = API_URL +"/hourly10day/q/pws:"+station+".json"
        hour_json = json.loads(get_api_data(url))

        filter_data = list()
        for hour_data in hour_json['hourly_forecast']:
            if hour_data['FCTTIME']['epoch'] >= epochstart and \
               hour_data['FCTTIME']['epoch'] <= epochend:
                filter_data.append(hour_data)


        json_response = json.dumps(filter_data)

        return HttpResponse(json_response)


class DailyForecast(View):
    def get(self,request,station,epochstart,epochend):
        url = API_URL +"/forecast10day/q/pws:"+station+".json"
        daily_json = json.loads(get_api_data(url))

        filter_data = list()
        for daily_data in daily_json['forecast']['simpleforecast']['forecastday']:
            if daily_data['date']['epoch'] >= epochstart and \
               daily_data['date']['epoch'] <= epochend:
                filter_data.append(daily_data)


        json_response = json.dumps(filter_data)

        return HttpResponse(json_response)

class CountryList(View):
    def get(self,request):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(dir_path,"static","country-city.json")
        with open(json_path) as data_json:
            country_json = data_json.read().replace("\\","\w")

        country_dict = json.loads(country_json)
        country_list = country_dict.keys()

        return HttpResponse(json.dumps(country_list))

class CityList(View):
    def get(self,request,country):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(dir_path,"static","country-city.json")
        with open(json_path) as data_json:
            country_json = data_json.read().replace("\\","\w")

        country_dict = json.loads(country_json)
        city_list = country_dict[country]

        return HttpResponse(json.dumps(city_list))