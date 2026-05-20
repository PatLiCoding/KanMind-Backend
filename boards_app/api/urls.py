from django.urls import path
from .views import BoardViewSet, EmailCheckView

board_list = BoardViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

board_detail = BoardViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('boards/', board_list, name='boards-list'),
    path('boards/<int:pk>/', board_detail, name='boards-detail'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]
