"""
URL configuration for todoapp project.

Maps URL patterns from the tasks app to the main project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('redirect/', RedirectView.as_view(url='/', permanent=False)),
]
