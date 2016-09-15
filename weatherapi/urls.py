__author__ = 'shaur'

from django.conf.urls import url

from views import StationList,DailyForecast,HourlyForecast,CountryList,CityList

urlpatterns = [
    url(r'^station-list/(?P<country>\w{0,50})/(?P<city>\w{0,50})', StationList.as_view(), name="station-list"),
     url(r'^country-list/', CountryList.as_view(), name="country-list"),
     url(r'^city-list/(?P<country>\w{0,50})/', CityList.as_view(), name="city-list"),
    url(r'^hourly-forecast/(?P<station>\w{0,50})/(?P<epochstart>\w{0,50})/(?P<epochend>\w{0,50})', HourlyForecast.as_view(), name="hourly-forecast"),
    url(r'^daily-forecast/(?P<station>\w{0,50})/(?P<epochstart>\w{0,50})/(?P<epochend>\w{0,50})', DailyForecast.as_view(), name="daily-forecast"),
]
