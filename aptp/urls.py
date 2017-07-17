from django.conf.urls import url, static
from aptm import settings
from .views import (AppEventDetailView, AppEventDetailListView,
                    AppEventDetailDetailView, AppHouseSuccessView,
                    AppOrderListView, AppOrderInfoView, FollowView,AppEventDetailUnitListView,
                    AppEventDetailRoomListView)

urlpatterns = [
    url(r'^(?P<pk>\d+)/detail/', AppEventDetailView.as_view(),
        name='app_eventdetail'),
    url(r'^(?P<pk>\d+)/houses/', AppEventDetailListView.as_view(),
        name='app_house_list'),
    url(r'^unit/',AppEventDetailUnitListView.as_view()),
    url(r'^room/',AppEventDetailRoomListView.as_view()),
    url(r'^follow/', FollowView.as_view(), name='app_follow_view'),
    url(r'^house/(?P<pk>\d+)/$', AppEventDetailDetailView.as_view(),
        name='app_house_info'),
    url(r'^house/(?P<pk>\d+)/success/', AppHouseSuccessView.as_view(),
        name='app_house_success'),
    url(r'^customer/(?P<pk>\d+)/orders', AppOrderListView.as_view(),
        name='app_order_list'),
    url(r'^order/(?P<pk>\d+)', AppOrderInfoView.as_view(),
        name='app_order_info'),
]
