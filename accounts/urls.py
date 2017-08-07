from django.conf.urls import url
from accounts.views import (LoginView,
                            LogoutView,
                            PersonalSettingsView,
                            CustomerLoginView,
                            DeleteTestView,
                            ImportView,
                            GetCustomerInfo,
                            CustomerLogoutView)

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='acc_login'),
    url(r'^settings/', PersonalSettingsView.as_view(), name='acc_settings'),
    url(r'^logout/', LogoutView.as_view(), name='acc_logout'),
    url(r'^cuslog/', CustomerLoginView.as_view(), name='acc_cuslog'),
    url(r'^cusout/', CustomerLogoutView.as_view(), name='acc_cuslog'),
    url(r'^ctdelete/', DeleteTestView.as_view(), name='acc_delete'),
    url(r'^import/', ImportView.as_view(), name='acc_import'),
    url(r'^info/', GetCustomerInfo.as_view()),
]
