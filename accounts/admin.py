from django.contrib import admin
from accounts.models import User
from apt.models import Company


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_admin')


admin.site.register(User, UserAdmin)
admin.site.register(Company)
