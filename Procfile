release: python manage.py migrate && python manage.py create_admin --username admin --email admin@todoapp.com --password changeme123
web: gunicorn todoapp.wsgi
