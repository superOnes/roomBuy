
from django.conf.urls import url

from backstage.views import LoginView, HomeListView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='bms_login'),
    url(r'^$', HomeListView.as_view(), name='bms_home'),
]
