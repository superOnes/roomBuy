from django.conf.urls import url
from django.views.generic import TemplateView
from .views import (
    EventListView,
    EventCreateView,
    ImportPriceView,
    ExportView,
    ExportCustomerView,
    EventUpdateView,
    EventDetailView,
    EventDetailListView,
    EventDetailTotalUpdateView,
    EventTermUpdateView,
    url2qrcode,
    EventDetailCreateView,
    EventDetailRemarkUpdateView,
    CustomListView, CustomCreateView,
    EventStatus, EventDelStatus,
    EventDelDel, DeleteCustomerView,
    ExportHouseHotView, HouseHeatView)


urlpatterns = [



    url(r'^qrcode/(.+)', url2qrcode, name='qrcode'),
    # 活动
    url(r'^pubstatus/', EventStatus.as_view(), name='event_status'),
    url(r'^list/', EventListView.as_view(), name='event_list'),
    url(r'^create/', EventCreateView.as_view(), name='event_create'),
    url(r'^importprice/', ImportPriceView.as_view(), name='event_import'),
    url(r'^(?P<pk>\d+)/$', EventDetailView.as_view(), name='event_detail'),
    url(r'^update/(?P<pk>\d+)/$',
        EventUpdateView.as_view(),
        name='event_update'),
    url(r'^update/(?P<pk>\d+)/term/',
        EventTermUpdateView.as_view(),
        name='event_term_update'),
    # 车位房源
    url(r'^^(?P<pk>\d+)/salestatus/', EventDelStatus.as_view(), name='eventdel_status'),
    url(r'^eventdeldel/$', EventDelDel.as_view(), name='eventdel_del'),
    url(r'^(?P<pk>\d+)/rooms/create/',
        EventDetailCreateView.as_view(),
        name='room_create'),
    url(r'^room/(?P<pk>\d+)/remark/',
        EventDetailRemarkUpdateView.as_view(),
        name='room_remark_update'),
    url(r'^(?P<pk>\d+)/rooms/$', EventDetailListView.as_view(), name='room_list'),
    url(r'^room/(?P<pk>\d+)/price/',
        EventDetailTotalUpdateView.as_view(),
        name='room_price_update'),
    url(r'^(?P<pk>\d+)/export/', ExportView.as_view(), name='room_export'),
    url(r'^househeat/', HouseHeatView.as_view(), name='househeat'),
    # 认筹
    url(r'^(?P<pk>\d+)/customs/$',
        CustomListView.as_view(),
        name='event_customs'),
    url(r'^(?P<pk>\d+)/customs/create/',
        CustomCreateView.as_view(),
        name='custom_create'),
    url(r'^(?P<pk>\d+)/cusexport/',
        ExportCustomerView.as_view(),
        name='customer_export'),
    url(r'^deletect/', DeleteCustomerView.as_view(), name='ct_delete'),
    url(r'^exporthousehot/', ExportHouseHotView.as_view(), name='househot_export'),
    url(r'^opensta/',TemplateView.as_view(template_name='opensta.html'), name='event_opensta'),
]
