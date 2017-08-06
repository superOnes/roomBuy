from django.conf.urls import url
from .views import (
    ProTimeView,
    AppEventDetailView,
    AppEventDetailListView,
    AppEventDetailHouseInfoView,
    AddFollow,
    CancelFollow,
    AppHouseChoiceConfirmView,
    AppOrderListView,
    AppOrderInfoView,
    FollowView,
    AppEventDetailUnitListView,
    AppEventDetailHouseListView,
    OrderProView, AppHouseChoiceConfirmTestView)

urlpatterns = [
    url(r'^detail/', AppEventDetailView.as_view(), name='app_eventdetail'),
    url(r'^houses/', AppEventDetailListView.as_view(), name='app_building_list'),
    url(r'^protime/', ProTimeView.as_view(), name='app_protocol_detail'),
    url(r'^unit/', AppEventDetailUnitListView.as_view(), name='app_unit_list'),
    url(r'^houselist/$', AppEventDetailHouseListView.as_view(), name='app_house_list'),
    url(r'^houseinfo/', AppEventDetailHouseInfoView.as_view(), name='app_house_info'),
    url(r'^addfollow/', AddFollow.as_view(), name='app_house_follow'),
    url(r'^cancelfollow/', CancelFollow.as_view(), name='app_house_cancelfollow'),
    url(r'^followlist/', FollowView.as_view(), name='app_follow_view'),
    url(r'^orderconfirm/', AppHouseChoiceConfirmView.as_view(), name='app_follow_view'),
    url(r'^orderinfo/', AppOrderInfoView.as_view(), name='app_order_info'),
    url(r'^orderpro/', OrderProView.as_view(), name='app_order_pro'),
    url(r'^orderslist', AppOrderListView.as_view(), name='app_order_list'),
    # 订单确认测试接口
    url(r'^orderconfirmtest/', AppHouseChoiceConfirmTestView.as_view()),
]
