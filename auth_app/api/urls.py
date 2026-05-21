"""
URL routing configuration for user authentication.

Endpoints:
    - POST /registration/ : Registers a new user account and creates an auth
                            token.
    - POST /login/        : Authenticates credentials and returns user data
                            + token.
"""

from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
]
