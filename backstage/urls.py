
from django.conf.urls import url

from backstage.views import LoginView, HomeListView,CreateView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^userlist/$', HomeListView.as_view(), name='home'),
    url(r'^createuser/$', CreateView.as_view(), name='createuser'),
]
