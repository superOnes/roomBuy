
from django.conf.urls import url

from backstage.views import LoginView, HomeListView, CreateView,\
    GetProvinceView, GetCityView, DeleteUserView, ModifyUserView,\
    PasswordResetView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^$', HomeListView.as_view(), name='home'),
    url(r'^createuser/$', CreateView.as_view(), name='createuser'),
    url(r'^getprovince/$', GetProvinceView.as_view(), name='get_province'),
    url(r'^getcity/$', GetCityView.as_view(), name='get_city'),
    url(r'^modify/$', ModifyUserView.as_view(), name='modify'),
    url(r'^reset/$', PasswordResetView.as_view(), name='reset'),
    url(r'^delete/$', DeleteUserView.as_view(), name='delete')
]
