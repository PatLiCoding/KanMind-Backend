from django.contrib import admin
from django.db.models import Count
from .models import Board


class BoardAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Board model.

    Provides custom query optimization via annotation to display aggregated
    member counts, filters boards by owner, and manages board members
    using a horizontal split-box widget.
    """
    list_display = ('title', 'owner', 'members_count')
    search_fields = ('title', 'owner__fullname')
    list_filter = ('owner',)
    filter_horizontal = ('members',)
    readonly_fields = ['owner']

    def get_queryset(self, request):
        """
        Extends the default admin queryset to pre-calculate the number of
        members mapped to each board via Django's Count aggregation.
        """
        queryset = super().get_queryset(request)
        return queryset.annotate(members_count=Count('members'))

    def members_count(self, obj):
        """
        Retrieves the annotated member count value for display in the list
        view.
        """
        return obj.members_count

    def save_model(self, request, obj, form, change):
        """
        Saves the Board instance, automatically assigning the logged-in
        admin user as the permanent owner during initial creation.
        """
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Board, BoardAdmin)
