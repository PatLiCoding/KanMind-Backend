from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.


class UserAdmin(UserAdmin):
    list_display = ('email', 'fullname', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('fullname',)}),
    )


admin.site.register(User, UserAdmin)
