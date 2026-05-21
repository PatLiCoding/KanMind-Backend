"""
Main URL configuration for the core project.

This module defines the top-level routing entry points. It mounts the
Django administration panel and includes the consolidated API endpoints
under the shared 'api/' prefix.

Top-Level Path Mapping:
    - /admin/    -> Django Administrative Control Panel
    - /api/     -> Core Project API Endpoints (Auth, Boards, Tasks, Comments)
"""

from django.contrib import admin
from django.urls import path, include
from .router import urlpatterns as api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]
