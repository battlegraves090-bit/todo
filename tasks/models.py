"""
Models for the tasks application.

Defines the Task model for managing user to-do items.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class Task(models.Model):
    """
    Task model representing a to-do item for a user.
    
    Attributes:
        user (ForeignKey): The user who owns this task
        title (CharField): The task title
        description (TextField): Optional detailed description
        due_date (DateField): Optional due date for the task
        priority (CharField): Priority level (Low/Medium/High)
        completed (BooleanField): Whether the task is completed
        created_at (DateTimeField): When the task was created
        updated_at (DateTimeField): When the task was last updated
    """
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text='The user who owns this task'
    )
    
    title = models.CharField(
        max_length=255,
        help_text='The title of the task'
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Optional description for the task'
    )
    
    due_date = models.DateField(
        blank=True,
        null=True,
        help_text='Optional due date for the task'
    )
    
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text='Priority level of the task'
    )
    
    completed = models.BooleanField(
        default=False,
        help_text='Whether the task is completed'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When the task was created'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='When the task was last updated'
    )
    
    class Meta:
        """Meta options for the Task model."""
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'completed']),
        ]
    
    def __str__(self):
        """Return the string representation of the task."""
        return f"{self.title} - {self.get_priority_display()}"
    
    def is_overdue(self):
        """
        Check if the task is overdue.
        
        Returns:
            bool: True if task has a due date and it's in the past and not completed
        """
        if self.due_date and not self.completed:
            return self.due_date < timezone.now().date()
        return False
    
    def days_until_due(self):
        """
        Calculate days until due date.
        
        Returns:
            int or None: Number of days until due date, or None if no due date
        """
        if self.due_date:
            delta = self.due_date - timezone.now().date()
            return delta.days
        return None


class UserProfile(models.Model):
    """
    Extended user profile for additional user information.
    
    Attributes:
        user (OneToOneField): The associated Django user
        bio (TextField): Optional user biography
        updated_at (DateTimeField): When the profile was last updated
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text='The associated Django user'
    )
    
    bio = models.TextField(
        blank=True,
        null=True,
        max_length=500,
        help_text='Optional user biography'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='When the profile was last updated'
    )
    
    class Meta:
        """Meta options for the UserProfile model."""
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        """Return the string representation of the user profile."""
        return f"{self.user.username}'s Profile"
