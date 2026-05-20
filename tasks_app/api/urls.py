from django.urls import path
from .views import TaskViewSet, CommentViewSet, \
    AssignedView, ReviewersView

tasks_list = TaskViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

tasks_detail = TaskViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

comment_detail = CommentViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('tasks/', tasks_list, name='tasks-list'),
    path('tasks/assigned-to-me/',
         AssignedView.as_view(), name='assigned'),
    path('tasks/reviewing/',
         ReviewersView.as_view(), name='reviewing'),
    path('tasks/<int:pk>/',
         tasks_detail, name='tasks-detail'),
    path('tasks/<int:pk>/comments/',
         comment_list, name='comment-list'),
    path('tasks/<int:pk>/comments/<int:comment_pk>/',
         comment_detail, name='comment-detail'),
]
