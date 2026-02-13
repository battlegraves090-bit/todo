"""
Forms for user authentication and task management.

Includes forms for:
- User registration
- User login (built-in Django)
- Task creation and editing
- User profile management
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import Task, UserProfile


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration with email field.
    
    Extends Django's UserCreationForm to include email field
    and provide custom styling.
    """
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email',
            'autocomplete': 'email'
        })
    )
    
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Choose a username',
            'autocomplete': 'username'
        })
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter password',
            'autocomplete': 'new-password'
        })
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password'
        })
    )
    
    class Meta:
        """Meta options for the registration form."""
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        """Validate that email is unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email
    
    def clean_username(self):
        """Validate that username is unique."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username


class UserEditForm(forms.ModelForm):
    """
    Form for editing user profile information.
    
    Allows users to update their username and email.
    """
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email address'
        })
    )
    
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First name (optional)'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last name (optional)'
        })
    )
    
    class Meta:
        """Meta options for the edit form."""
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with user-specific data."""
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('instance')
    
    def clean_email(self):
        """Validate that email is unique (excluding current user)."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This email is already registered.')
        return email
    
    def clean_username(self):
        """Validate that username is unique (excluding current user)."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This username is already taken.')
        return username


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile bio.
    """
    
    bio = forms.CharField(
        label='Bio',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Tell us about yourself...',
            'rows': 4
        })
    )
    
    class Meta:
        """Meta options for the profile form."""
        model = UserProfile
        fields = ('bio',)


class TaskForm(forms.ModelForm):
    """
    Form for creating and editing tasks.
    
    Provides fields for task title, description, due date, and priority.
    """
    
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Task title',
            'required': True
        })
    )
    
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Task description (optional)',
            'rows': 3
        })
    )
    
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date'
        })
    )
    
    priority = forms.ChoiceField(
        choices=Task.PRIORITY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    class Meta:
        """Meta options for the task form."""
        model = Task
        fields = ('title', 'description', 'due_date', 'priority')
    
    def clean_title(self):
        """Validate that title is not empty after stripping whitespace."""
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError('Task title cannot be empty.')
        return title


class TaskFilterForm(forms.Form):
    """
    Form for filtering tasks.
    
    Allows users to filter by completion status, priority, and search text.
    """
    
    STATUS_CHOICES = [
        ('all', 'All Tasks'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    
    PRIORITY_FILTER = [
        ('', 'All Priorities'),
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        initial='all',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'status-filter'
        })
    )
    
    priority = forms.ChoiceField(
        choices=PRIORITY_FILTER,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'priority-filter'
        })
    )
    
    search = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Search tasks...',
            'id': 'search-input'
        })
    )


class UserDeleteForm(forms.Form):
    """
    Form for confirming account deletion.
    
    Requires user to enter their password to delete their account.
    """
    
    password = forms.CharField(
        label='Confirm your password to delete your account',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password'
        })
    )
    
    confirm = forms.BooleanField(
        label='I understand that this action cannot be undone',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox',
            'required': True
        })
    )
