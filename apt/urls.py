from django.conf.urls import url
from django.views.generic import TemplateView
from accounts.decorators import admin_required
from .views import (EventListView, EventCreateView, ImportEventDetailView,
                    ExportEventDetailView, ExportCustomerView, EventUpdateView,
                    EventDetailView, EventDetailListView,
                    EventDetailPriceUpdateView, EventTermUpdateView,
                    EventDetailCreateView,
                    EventDetailRemarkUpdateView, CustomListView,
                    CustomCreateView, EventStatus, EventDetailStatus,
                    EventDetailDel,
                    CustomerDeleteView, ExportHouseHotView, HouseHeatView,
                    HouseTypeListView, HouseTypeCreateView,
                    HouseTypeUpdateView, CustomerCountUpdateView,
                    ExportBuyHotView, HouseTypeRelatedView,
                    EventDetailHTUpdateView, PurcharseHeatView, GetEventView,
                    OrderListView, EventDetailSignUpdateView,
                    DeleteHouseTypeView, ExportOrderView)


urlpatterns = [
    # 活动
    url(r'^$', EventListView.as_view(), name='event_list'),
    url(r'^create/', EventCreateView.as_view(), name='event_create'),
    url(r'^(?P<pk>\d+)/$', EventDetailView.as_view(), name='event_detail'),
    url(r'^(?P<pk>\d+)/update/$', EventUpdateView.as_view(),
        name='event_update'),
    url(r'^(?P<pk>\d+)/termupdate/', EventTermUpdateView.as_view(),
        name='event_term_update'),
    url(r'^pubstatus/', EventStatus.as_view(), name='event_status'),

    # 车位房源
    url(r'^(?P<pk>\d+)/rooms/$', EventDetailListView.as_view(),
        name='room_list'),
    url(r'^(?P<pk>\d+)/rooms/create/', EventDetailCreateView.as_view(),
        name='room_create'),
    url(r'^room/(?P<pk>\d+)/price/', EventDetailPriceUpdateView.as_view(),
        name='room_price_update'),
    url(r'^room/(?P<pk>\d+)/remark/', EventDetailRemarkUpdateView.as_view(),
        name='room_remark_update'),
    url(r'^room/(?P<pk>\d+)/sign/', EventDetailSignUpdateView.as_view(),
        name='room_sign_update'),
    url(r'^room/(?P<pk>\d+)/ht/', EventDetailHTUpdateView.as_view(),
        name='room_ht_update'),
    url(r'^(?P<pk>\d+)/salestatus/', EventDetailStatus.as_view()),
    url(r'^eventdetaildel/$', EventDetailDel.as_view()),
    url(r'^import/rooms/', ImportEventDetailView.as_view()),
    url(r'^(?P<pk>\d+)/export/rooms/', ExportEventDetailView.as_view(),
        name='room_export'),

    # 认筹名单
    url(r'^(?P<pk>\d+)/customs/$', CustomListView.as_view(),
        name='event_customs'),
    url(r'^(?P<pk>\d+)/customs/create/', CustomCreateView.as_view(),
        name='custom_create'),
    url(r'^customs/(?P<pk>\d+)/count', CustomerCountUpdateView.as_view(),
        name='customer_count_update'),
    url(r'^customer/delete/', CustomerDeleteView.as_view()),
    url(r'^(?P<pk>\d+)/export/customer/', ExportCustomerView.as_view(),
        name='customer_export'),

    # 户型
    url(r'^(?P<pk>\d+)/housetypes/$', HouseTypeListView.as_view(),
        name='event_house_type_list'),
    url(r'^(?P<pk>\d+)/housetypes/create', HouseTypeCreateView.as_view(),
        name='event_house_type_create'),
    url(r'^housetypes/(?P<pk>\d+)/update', HouseTypeUpdateView.as_view(),
        name='event_house_type_update'),
    url(r'^housetypes/', HouseTypeRelatedView.as_view(),
        name='event_house_type_related'),
    url(r'^dlhousetypes/', DeleteHouseTypeView.as_view(),
        name='delete_house_type'),

    # 开盘统计管理
    url(r'^opensta/', admin_required(TemplateView.as_view(template_name='opensta.html')),
        name='event_opensta'),
    url(r'^househeat/', HouseHeatView.as_view()),
    url(r'^purcharseheat/', PurcharseHeatView.as_view()),
    url(r'^getevent/', GetEventView.as_view()),
    url(r'^export/househot/', ExportHouseHotView.as_view()),
    url(r'^export/buyhot/', ExportBuyHotView.as_view()),

    # 开盘订单管理
    url(r'^order/', admin_required(TemplateView.as_view(template_name='order.html')),
        name='event_order'),
    url(r'^orderlist/', OrderListView.as_view(), name='orderlist'),
    url(r'^exportorder/', ExportOrderView.as_view()),
]
