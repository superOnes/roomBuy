from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from accounts.models import User
from apt.models import Company


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'is_admin', 'password1', 'password2',
                  'expire_date', 'house_limit', 'company')


class MyUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'is_admin', 'password', 'house_limit',
                  'expire_date', 'company')


class MyUserAdmin(UserAdmin):

    form = MyUserChangeForm
    add_form = MyUserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'is_admin', 'password', 'house_limit',
                           'expire_date', 'company')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'is_admin', 'password1', 'password2',
                       'house_limit', 'expire_date', 'company')}
         ),
    )


admin.site.register(User, MyUserAdmin)
admin.site.register(Company)
