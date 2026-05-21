from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.


class UserAdmin(UserAdmin):
    """
    Custom admin configuration for the User model.

    Extends the built-in Django UserAdmin to display and manage
    the custom 'fullname' field inside the Django Admin panel.
    """
    list_display = ('email', 'fullname', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('fullname',)}),
    )


admin.site.register(User, UserAdmin)
