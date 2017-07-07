from django.conf.urls import url
from .views import HomePageView,HouseDetailView

urlpatterns=[
    url(r'^homepage/',HomePageView.as_view(),name='home_page_view'),
    url(r'^housedel/',HouseDetailView.as_view(),name='aptp_eventdel'),
]