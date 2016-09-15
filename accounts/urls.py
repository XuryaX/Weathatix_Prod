from django.conf.urls import url


from views import RegistrationView,LoginView,LogoutView

urlpatterns = [
    url(r'^register/', RegistrationView.as_view(), name="register-user"),
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'^logout/', LogoutView.as_view(), name="logout"),
]
