from django.conf.urls import url
from .views import EventListView

urlpatterns = [
    url(r'^list/', EventListView.as_view(), name='event_list'),
]
