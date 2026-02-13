"""
Views for the tasks application.

Includes views for:
- User authentication (register, login, logout)
- Task management (list, create, update, delete)
- User profile management
- Dashboard and statistics
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
)
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_control
import json
from datetime import datetime, timedelta

from .models import Task, UserProfile
from .forms import (
    UserRegistrationForm, UserEditForm, UserProfileForm,
    TaskForm, TaskFilterForm, UserDeleteForm
)


# ============================================================================
# CUSTOM MIXINS
# ============================================================================

class NoCacheLoginRequiredMixin(LoginRequiredMixin):
    """
    Mixin that combines LoginRequired with cache prevention.
    
    Ensures authenticated pages are never cached by the browser,
    preventing users from accessing cached versions after logout.
    """
    
    def dispatch(self, request, *args, **kwargs):
        """Apply cache control before processing the view."""
        response = super().dispatch(request, *args, **kwargs)
        # Prevent any caching of authenticated pages
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, private, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


# ============================================================================
# AUTHENTICATION VIEWS
# ============================================================================

class RegisterView(CreateView):
    """
    View for user registration.
    
    Allows new users to create an account with username, email, and password.
    """
    form_class = UserRegistrationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Register'
        return context
    
    def form_valid(self, form):
        """Handle successful registration."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Registration successful! Please log in to your account.'
        )
        return response


class CustomLoginView(LoginView):
    """
    Custom login view with improved user experience.
    
    Handles user authentication and redirects to dashboard on success.
    """
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Login'
        return context
    
    def form_valid(self, form):
        """Handle successful login."""
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """
    Custom logout view with session termination and cache control.
    
    Ensures complete session cleanup and prevents cached pages from being visible.
    """
    next_page = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        """
        Handle logout with explicit session clearing and cache control.
        
        - Displays success message
        - Clears all session data
        - Sets cache control headers
        - Redirects to login page
        """
        # Log the logout action
        if request.user.is_authenticated:
            username = request.user.username
            messages.success(request, f'You have been logged out successfully, {username}.')
        else:
            messages.success(request, 'You have been logged out successfully.')
        
        # Call parent dispatch to handle the logout
        response = super().dispatch(request, *args, **kwargs)
        
        # Explicitly flush the session to ensure complete cleanup
        if hasattr(request, 'session'):
            request.session.flush()
        
        # Set cache control headers to prevent browser from caching authenticated pages
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, private, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        return response


# ============================================================================
# PROFILE MANAGEMENT VIEWS
# ============================================================================

class ProfileView(NoCacheLoginRequiredMixin, TemplateView):
    """
    View for displaying and managing user profile.
    
    Displays user information and provides options to edit profile,
    change password, or delete account.
    """
    template_name = 'tasks/profile.html'
    
    def get_context_data(self, **kwargs):
        """Prepare context with user data and forms."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)
        
        context['page_title'] = 'My Profile'
        context['user'] = user
        context['profile'] = profile
        context['edit_form'] = UserEditForm(instance=user)
        context['profile_form'] = UserProfileForm(instance=profile)
        context['password_form'] = PasswordChangeForm(user)
        context['delete_form'] = UserDeleteForm()
        
        # Task statistics
        tasks = Task.objects.filter(user=user)
        context['total_tasks'] = tasks.count()
        context['completed_tasks'] = tasks.filter(completed=True).count()
        context['pending_tasks'] = tasks.filter(completed=False).count()
        
        return context


class EditProfileView(NoCacheLoginRequiredMixin, View):
    """
    View for handling profile edit form submission.
    """
    
    def post(self, request):
        """Handle profile edit form submission."""
        form = UserEditForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('profile')


class EditProfileBioView(NoCacheLoginRequiredMixin, View):
    """
    View for updating user bio/profile information.
    """
    
    def post(self, request):
        """Handle bio update."""
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(request.POST, instance=profile)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Bio updated successfully!')
        else:
            messages.error(request, 'Error updating bio.')
        
        return redirect('profile')


class ChangePasswordView(NoCacheLoginRequiredMixin, View):
    """
    View for handling password change.
    """
    
    def post(self, request):
        """Handle password change form submission."""
        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
            return redirect('profile')


class DeleteAccountView(NoCacheLoginRequiredMixin, View):
    """
    View for handling account deletion.
    
    Requires password confirmation before deleting account.
    """
    
    def post(self, request):
        """Handle account deletion with password confirmation."""
        form = UserDeleteForm(request.POST)
        
        if form.is_valid():
            if request.user.check_password(form.cleaned_data['password']):
                user = request.user
                username = user.username
                user.delete()
                messages.success(
                    request,
                    f'Account {username} has been deleted successfully.'
                )
                return redirect('login')
            else:
                messages.error(request, 'Incorrect password. Account not deleted.')
        
        return redirect('profile')


# ============================================================================
# DASHBOARD AND STATISTICS
# ============================================================================

class DashboardView(NoCacheLoginRequiredMixin, TemplateView):
    """
    Main dashboard view showing task overview and statistics.
    
    Displays task summary, quick stats, and task list preview.
    """
    template_name = 'tasks/dashboard.html'
    
    def get_context_data(self, **kwargs):
        """Prepare dashboard context with task statistics."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get user's tasks
        tasks = Task.objects.filter(user=user)
        
        # Calculate statistics
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(completed=True).count()
        pending_tasks = tasks.filter(completed=False).count()
        high_priority_tasks = tasks.filter(priority='high', completed=False).count()
        
        # Get overdue tasks
        today = datetime.now().date()
        overdue_tasks = tasks.filter(
            due_date__lt=today,
            completed=False
        ).count()
        
        # Get tasks due today
        due_today = tasks.filter(
            due_date=today,
            completed=False
        ).count()
        
        # Completion percentage
        completion_percentage = (
            (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        )
        
        context.update({
            'page_title': 'Dashboard',
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'high_priority_tasks': high_priority_tasks,
            'overdue_tasks': overdue_tasks,
            'due_today': due_today,
            'completion_percentage': int(completion_percentage),
            'recent_tasks': tasks[:5],
        })
        
        return context


# ============================================================================
# TASK MANAGEMENT VIEWS
# ============================================================================

class TaskListView(NoCacheLoginRequiredMixin, ListView):
    """
    View for displaying list of user's tasks with filtering options.
    
    Supports filtering by completion status, priority, and search query.
    """
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20
    
    def get_queryset(self):
        """Get filtered task queryset based on user input."""
        user = self.request.user
        queryset = Task.objects.filter(user=user)
        
        # Filter by status
        status = self.request.GET.get('status', 'all')
        if status == 'completed':
            queryset = queryset.filter(completed=True)
        elif status == 'pending':
            queryset = queryset.filter(completed=False)
        
        # Filter by priority
        priority = self.request.GET.get('priority', '')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Search by title or description
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """Add filters and statistics to context."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        tasks = Task.objects.filter(user=user)
        
        context['page_title'] = 'Tasks'
        context['filter_form'] = TaskFilterForm(self.request.GET)
        context['total_tasks'] = tasks.count()
        context['completed_tasks'] = tasks.filter(completed=True).count()
        context['pending_tasks'] = tasks.filter(completed=False).count()
        context['current_status'] = self.request.GET.get('status', 'all')
        context['current_priority'] = self.request.GET.get('priority', '')
        context['search_query'] = self.request.GET.get('search', '')
        
        return context


class TaskCreateView(NoCacheLoginRequiredMixin, CreateView):
    """
    View for creating a new task.
    
    Renders a form for users to input task details and creates the task
    associated with the logged-in user.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        """Associate task with current user before saving."""
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        messages.success(self.request, f'Task "{task.title}" created successfully!')
        return redirect('task_list')
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Task'
        context['form_title'] = 'Create New Task'
        return context


class TaskUpdateView(NoCacheLoginRequiredMixin, UpdateView):
    """
    View for editing an existing task.
    
    Only allows users to edit their own tasks.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')
    
    def get_queryset(self):
        """Only allow user to edit their own tasks."""
        return Task.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        """Handle successful task update."""
        task = form.save()
        messages.success(self.request, f'Task "{task.title}" updated successfully!')
        return redirect('task_list')
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit Task'
        context['form_title'] = 'Edit Task'
        return context


class TaskDeleteView(NoCacheLoginRequiredMixin, DeleteView):
    """
    View for deleting a task.
    
    Only allows users to delete their own tasks.
    """
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
    
    def get_queryset(self):
        """Only allow user to delete their own tasks."""
        return Task.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        """Add success message and delete the task."""
        task = self.get_object()
        task_title = task.title
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Task "{task_title}" deleted successfully!')
        return response
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Delete Task'
        return context


# ============================================================================
# AJAX API ENDPOINTS FOR DYNAMIC UPDATES
# ============================================================================

@require_http_methods(["POST"])
def toggle_task_status(request, task_id):
    """
    AJAX endpoint to toggle task completion status.
    
    Returns JSON response with success status and updated task data.
    """
    try:
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.completed = not task.completed
        task.save()
        
        return JsonResponse({
            'success': True,
            'completed': task.completed,
            'message': 'Task status updated.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@require_http_methods(["POST"])
def quick_add_task(request):
    """
    AJAX endpoint for quick task creation.
    
    Creates a task with just a title. Used for rapid task entry.
    Returns JSON response with the created task data.
    """
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        
        if not title:
            return JsonResponse({
                'success': False,
                'message': 'Task title is required.'
            }, status=400)
        
        task = Task.objects.create(
            user=request.user,
            title=title,
            priority='medium'
        )
        
        return JsonResponse({
            'success': True,
            'task_id': task.id,
            'title': task.title,
            'created_at': task.created_at.isoformat(),
            'message': 'Task created successfully!'
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request format.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@require_http_methods(["POST"])
def delete_task_ajax(request, task_id):
    """
    AJAX endpoint for deleting a task.
    
    Returns JSON response with success status.
    """
    try:
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task_title = task.title
        task.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Task "{task_title}" deleted successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@require_http_methods(["GET"])
def get_task_detail(request, task_id):
    """
    AJAX endpoint to get task details.
    
    Returns JSON response with task information.
    """
    try:
        task = get_object_or_404(Task, id=task_id, user=request.user)
        
        return JsonResponse({
            'success': True,
            'task': {
                'id': task.id,
                'title': task.title,
                'description': task.description or '',
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'priority': task.priority,
                'completed': task.completed,
                'created_at': task.created_at.isoformat(),
                'updated_at': task.updated_at.isoformat(),
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)
