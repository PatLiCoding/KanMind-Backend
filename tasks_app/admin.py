from django.contrib import admin
from .models import Task, Comments


class TaskAdmin(admin.ModelAdmin):
    list_filter = ['status', 'priority', 'board']
    list_display = ['title', 'board', 'status',
                    'priority', 'create_by', 'due_date']
    search_fields = ['title', 'description',
                     'create_by__email', 'create_by__fullname']
    readonly_fields = ['create_by']
    fieldsets = [
        ('Key Information', {
            'fields': ['board', 'title', 'description',
                       'status', 'priority', 'due_date']
        }),
        ('Responsibilities', {
            'classes': ['collapse'],
            'fields': ['create_by', 'assignee', 'reviewer']
        }),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_by = request.user
        super().save_model(request, obj, form, change)


class CommentsAdmin(admin.ModelAdmin):
    list_filter = ['author', 'created_at']
    list_display = ['author', 'task', 'created_at']
    readonly_fields = ['author']
    search_fields = ['content', 'author__email', 'author__fullname']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Task, TaskAdmin)
admin.site.register(Comments, CommentsAdmin)
