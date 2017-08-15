
from django.conf.urls import url

from backstage.views import LoginView, HomeListView,CreateView

urlpatterns = [
<<<<<<< HEAD
    url(r'^login/$', LoginView.as_view(), name='bms_login'),
    url(r'^$', HomeListView.as_view(), name='bms_home'),
=======
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^userlist/$', HomeListView.as_view(), name='home'),
    url(r'^createuser/$', CreateView.as_view(), name='createuser'),
>>>>>>> twp
]
