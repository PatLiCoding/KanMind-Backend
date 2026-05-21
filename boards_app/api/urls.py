"""
URL routing configuration for project boards and helper utilities.

Maps RESTful operations to the BoardViewSet and binds the EmailCheckView
lookup utility.

Endpoints:
    - GET  /boards/           : Lists all boards where the user is an owner
                                or member.
    - POST /boards/           : Creates a new board (assigns request user as
                                owner).
    - GET  /boards/<id>/      : Retrieves detailed data of a single board
                                including tasks.
    - PATCH /boards/<id>/     : Partially updates board details or members
                                list.
    - DELETE /boards/<id>/    : Destroys a board instance (restricted
                                to owners).
    - GET  /email-check/      : Looks up user ID and fullname by providing an
                                ?email= query param.
"""

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
