from django.urls import path
from .views import BoardsView

urlpatterns = [
    path('boards/', BoardsView.as_view(), name='boards'),
]
