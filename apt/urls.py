from django.conf.urls import url
from .views import EventListView,EventCreateView

urlpatterns = [
    url(r'^list/', EventListView.as_view(), name='event_list'),
    url(r'^create/', EventCreateView.as_view(), name='event_create'),
]
