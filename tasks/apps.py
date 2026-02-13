"""
Django app configuration for the tasks application.
"""

from django.apps import AppConfig


class TasksConfig(AppConfig):
    """Configuration class for the tasks app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    verbose_name = 'Task Management'
    
    def ready(self):
        """Initialize app-specific configurations."""
        import tasks.signals  # noqa: F401
