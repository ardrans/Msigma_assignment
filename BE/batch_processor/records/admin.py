from django.contrib import admin
from records.models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    """Admin configuration for Record model."""
    
    list_display = ['id', 'name', 'email', 'phone_number', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone_number', 'link', 'dob')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
