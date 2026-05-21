from django.contrib import admin
from django.db.models import Count
from .models import Board


class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'members_count')
    search_fields = ('title', 'owner__fullname')
    list_filter = ('owner',)
    filter_horizontal = ('members',)
    readonly_fields = ['owner']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(members_count=Count('members'))

    def members_count(self, obj):
        return obj.members_count

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Board, BoardAdmin)
