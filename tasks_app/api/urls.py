from django.urls import path
from .views import TaskView, TaskDetailView, \
    AssignedView, ReviewersView, CommentView, CommentDetailView

urlpatterns = [
    path('tasks/', TaskView.as_view(), name='tasks'),
    path('tasks/assigned-to-me/', 
         AssignedView.as_view(), name='assigned'),
    path('tasks/reviewing/', 
         ReviewersView.as_view(), name='reviewing'),
    path('tasks/<int:task_id>/', 
         TaskDetailView.as_view(), name='tasks-detail'),
    path('tasks/<int:task_id>/comments/', 
         CommentView.as_view(), name='tasks-detail'),   
    path('tasks/<int:task_id>/comments/<int:comment_id>/', 
         CommentDetailView.as_view(), name='comment-detail'),
]
