"""
Global API router assembly module.

This module initializes a base DRF SimpleRouter and dynamically aggregates
the modular URL patterns from auth_app, boards_app, and tasks_app into
a single combined list of endpoints.
"""

from rest_framework import routers
from auth_app.api.urls import urlpatterns as auth_urls
from boards_app.api.urls import urlpatterns as board_urls
from tasks_app.api.urls import urlpatterns as tasks_urls

router = routers.SimpleRouter()
urlpatterns = router.urls
urlpatterns.extend(auth_urls)
urlpatterns.extend(board_urls)
urlpatterns.extend(tasks_urls)
