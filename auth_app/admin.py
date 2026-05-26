from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import User

# Register your models here.


class CustomUserCreationForm(forms.ModelForm):
    """
    Form for creating users in the admin area.
    """
    password = forms.CharField(widget=forms.PasswordInput, label="Passwort")

    class Meta:
        model = User
        fields = ('email', 'fullname')

    def save(self, commit=True):
        """
        Saves the user instance after hashing the provided password.

        Args:
            commit (bool, optional): If True, saves the object to the database.
                                     Defaults to True.

        Returns:
            User: The saved or updated user model instance.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdmin(UserAdmin):
    """
    Custom admin configuration for the User model.

    Extends the built-in Django UserAdmin to display and manage
    the custom 'fullname' field inside the Django Admin panel.
    """
    add_form = CustomUserCreationForm
    ordering = ('email',)
    list_display = ('email', 'fullname', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Information', {'fields': ('fullname',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'password'),
        }),
    )


admin.site.register(User, UserAdmin)
