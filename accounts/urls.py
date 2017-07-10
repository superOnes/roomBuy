from django.conf.urls import url
from accounts.views import (LoginView,
                            LogoutView,
                            AccountStatusView,
                            PasswordResetView,
                            UserListView,
                            UserConfigView,
                            PersonalSettingsView,
                            CustomerLoginView,
                            )

urlpatterns = [

    # 接口
    url(r'^login/', LoginView.as_view(), name='acc_login'),
    url(r'^status/', AccountStatusView.as_view(), name='acc_status'),
    url(r'^reset/', PasswordResetView.as_view(), name='acc_reset'),
    url(r'^list/', UserListView.as_view(), name='acc_list'),
    url(r'^config/', UserConfigView.as_view(), name='acc_config'),
    url(r'^settings/', PersonalSettingsView.as_view(), name='acc_settings'),
    url(r'^logout/', LogoutView.as_view(), name='acc_logout'),
    url(r'^cuslog/', CustomerLoginView.as_view(), name='acc_cuslog'),
]
