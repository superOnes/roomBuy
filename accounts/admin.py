from django.contrib import admin
from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_admin')


admin.site.register(User, UserAdmin)
