from django.conf.urls import url
from .views import (AppLoginView, AppEventDetailView, AppEventDetailListView,
                    AppEventDetailDetailView, AppHouseSuccessView,
                    AppOrderListView, AppOrderInfoView)

urlpatterns = [
    url(r'^login/', AppLoginView.as_view(), name='app_login'),
    url(r'^(?P<pk>\d+)/detail/', AppEventDetailView.as_view(),
        name='app_eventdetail'),
    url(r'^(?P<pk>\d+)/houses/', AppEventDetailListView.as_view(),
        name='app_house_list'),
    url(r'^house/(?P<pk>\d+)/$', AppEventDetailDetailView.as_view(),
        name='app_house_info'),
    url(r'^house/(?P<pk>\d+)/success/', AppHouseSuccessView.as_view(),
        name='app_house_success'),
    url(r'^customer/(?P<pk>\d+)/orders', AppOrderListView.as_view(),
        name='app_order_list'),
    url(r'^order/(?P<pk>\d+)', AppOrderInfoView.as_view(),
        name='app_order_info'),
]
