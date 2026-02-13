"""
URL configuration for the tasks application.

Maps URL patterns to views for all task-related endpoints.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Task Management URLs
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    
    # Profile Management URLs
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('profile/edit-bio/', views.EditProfileBioView.as_view(), name='edit_profile_bio'),
    path('profile/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('profile/delete-account/', views.DeleteAccountView.as_view(), name='delete_account'),
    
    # AJAX API Endpoints
    path('api/tasks/<int:task_id>/toggle/', views.toggle_task_status, name='toggle_task_status'),
    path('api/tasks/quick-add/', views.quick_add_task, name='quick_add_task'),
    path('api/tasks/<int:task_id>/delete/', views.delete_task_ajax, name='delete_task_ajax'),
    path('api/tasks/<int:task_id>/detail/', views.get_task_detail, name='get_task_detail'),
]
