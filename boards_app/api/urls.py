from django.urls import path
from .views import BoardsView, BoardDetailView, EmailCheckView

urlpatterns = [
    path('boards/', BoardsView.as_view(), name='boards'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
    path('boards/<int:board_id>/', BoardDetailView.as_view(), name='boards-detail')
]
