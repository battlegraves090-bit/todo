"""
Django admin configuration for the tasks application.

Registers models and customizes admin interface for task management.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Task, UserProfile


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface for Task model.
    
    Provides a user-friendly interface for managing tasks in Django admin.
    """
    
    list_display = (
        'title',
        'user',
        'priority_badge',
        'completed_badge',
        'due_date',
        'created_at',
    )
    
    list_filter = (
        'completed',
        'priority',
        'created_at',
        'user',
    )
    
    search_fields = (
        'title',
        'description',
        'user__username',
    )
    
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    
    fieldsets = (
        ('Task Information', {
            'fields': ('user', 'title', 'description')
        }),
        ('Task Details', {
            'fields': ('due_date', 'priority', 'completed')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def priority_badge(self, obj):
        """Display priority as a colored badge."""
        colors = {
            'high': '#EF4444',
            'medium': '#F59E0B',
            'low': '#10B981',
        }
        color = colors.get(obj.priority, '#6B7280')
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 6px; font-size: 12px;">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
    
    def completed_badge(self, obj):
        """Display completion status as a badge."""
        if obj.completed:
            return format_html(
                '<span style="background-color: #10B981; color: white; '
                'padding: 3px 10px; border-radius: 6px; font-size: 12px;">✓ Completed</span>'
            )
        return format_html(
            '<span style="background-color: #94A3B8; color: white; '
            'padding: 3px 10px; border-radius: 6px; font-size: 12px;">○ Pending</span>'
        )
    completed_badge.short_description = 'Status'
    
    ordering = ('-created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    
    Allows admins to manage user profiles and bio information.
    """
    
    list_display = (
        'username',
        'email',
        'updated_at',
    )
    
    readonly_fields = (
        'user',
        'updated_at',
    )
    
    search_fields = (
        'user__username',
        'user__email',
    )
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('bio',)
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    def username(self, obj):
        """Display username from related user."""
        return obj.user.username
    username.short_description = 'Username'
    
    def email(self, obj):
        """Display email from related user."""
        return obj.user.email
    email.short_description = 'Email'
