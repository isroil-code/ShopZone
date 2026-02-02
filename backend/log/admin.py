from django.contrib import admin
from .models import ActivityLog
from django.utils.html import format_html

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'colored_action', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp', 'user')
    search_fields = ('user__username', 'action', 'details')
    readonly_fields = ('user', 'action', 'timestamp', 'details', 'ip_address', 'user_agent')
    ordering = ('-timestamp',)

    def colored_action(self, obj):
        colors = {
            'login': 'green',
            'logout': 'red',
            'view_product': 'blue',
            'create_product': 'purple',
            'update_product': 'orange',
            'delete_product': 'darkred',
            'create_order': 'teal',
            'admin_action': 'black',
            'other': 'gray',
        }
        color = colors.get(obj.action, 'gray')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_action_display())
    colored_action.short_description = 'Action'
