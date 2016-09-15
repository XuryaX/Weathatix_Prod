from django.conf.urls import url


from views import WeatherView,CreateStation,Subscribe

urlpatterns = [
    url(r'^$', WeatherView.as_view(),name="homepage"),
    url(r'add_station', CreateStation.as_view(),name="add-station"),
    url(r'^subscribe', Subscribe.as_view(),name="subscribe"),
]
