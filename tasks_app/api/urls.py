"""
URL routing configuration for tasks and nested comments management.

Manages task tracking queues and builds nested structural routes to isolate
comment threads within their respective parent tasks.

Endpoints:
    - GET  /tasks/
    : Lists accessible tasks filtered by workspace membership.
    - POST /tasks/
    : Creates a task bound to a cleared board.
    - GET  /tasks/assigned-to-me/
    : Lists tasks where the user is assigned.
    - GET  /tasks/reviewing/
    : Lists tasks where the user is a designated reviewer.
    - GET  /tasks/<id>/
    : Fetches full metrics of a single tasks
    - PATCH /tasks/<id>/
    : Partially modifies task state, assignees, or priority.
    - DELETE /tasks/<id>/
    : Drops a task (restricted to creator or board owner).
    - GET  /tasks/<id>/comments/
    : Fetches all comments posted on this task.
    - POST /tasks/<id>/comments/
    : Adds a new comment text thread under this task.
    - GET  /tasks/<id>/comments/<comment_id>/
    : Details a specific comment instance.
    - DELETE /tasks/<id>/comments/<comment_id>/
    : Deletes a specific comment (restricted to comment author).
"""

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
