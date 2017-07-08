from django.conf.urls import url
from .views import (
    EventListView,
    EventCreateView,
    ImportView,
    ExportView,
    EventUpdateView,
    EventDetailView,
    EventDetailListView,
    EventDetailTotalUpdateView,
    EventTermUpdateView,
    EventDetailCreateView,
    EventDetailRemarkUpdateView)


urlpatterns = [
    url(r'^list/', EventListView.as_view(), name='event_list'),
    url(r'^create/', EventCreateView.as_view(), name='event_create'),
    url(r'^import/', ImportView.as_view(), name='event_import'),
    url(r'^(?P<pk>\d+)/export/', ExportView, name='event_export'),
    url(r'^(?P<pk>\d+)/$', EventDetailView.as_view(), name='event_detail'),
    url(r'^update/(?P<pk>\d+)/$', EventUpdateView.as_view(),
        name='event_update'),
    url(r'^update/(?P<pk>\d+)/term/', EventTermUpdateView.as_view(),
        name='event_term_update'),
    # EventDetail
    url(r'^(?P<pk>\d+)/rooms/$', EventDetailListView.as_view(),
        name='room_list'),
    url(r'^(?P<pk>\d+)/rooms/create/', EventDetailCreateView.as_view(),
        name='room_create'),
    url(r'^room/(?P<pk>\d+)/price/', EventDetailTotalUpdateView.as_view(),
        name='room_price_update'),
    url(r'^room/(?P<pk>\d+)/remark/', EventDetailRemarkUpdateView.as_view(),
        name='room_remark_update'),


]
