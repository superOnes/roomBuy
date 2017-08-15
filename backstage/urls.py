
from django.conf.urls import url

from backstage.views import ManagerView

urlpatterns = [
    url(r'^manager/', ManagerView.as_view(), name='manager'),
]

