from django.urls import path
from .views import BoardsView, EmailCheckView

urlpatterns = [
    path('boards/', BoardsView.as_view(), name='boards'),
    path('email-check/', EmailCheckView.as_view(), name='email-check')
]
