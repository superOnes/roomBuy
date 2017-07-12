from django.conf.urls import url
from .views import AppLoginView, HomePageView, HouseDetailView

urlpatterns = [
    url(r'^login/', AppLoginView.as_view(), name='app_login'),
    url(r'^homepage/', HomePageView.as_view(), name='home_page_view'),
    url(r'^housedel/', HouseDetailView.as_view(), name='aptp_eventdel'),
]
