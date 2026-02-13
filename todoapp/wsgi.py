"""
WSGI config for todoapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoapp.settings')

application = get_wsgi_application()

# Run migrations on startup
def run_migrations():
    try:
        from django.db import connection
        # Check if database is accessible
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        # Run migrations if DB is ready
        call_command('migrate', '--noinput', verbosity=0)
        # Try to create admin if doesn't exist
        try:
            call_command('create_admin', '--username', 'admin', '--email', 'admin@todoapp.com', '--password', 'changeme123', verbosity=0)
        except Exception as e:
            print(f"Admin creation note: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Migration note: {e}", file=sys.stderr)

# Run on startup
run_migrations()
