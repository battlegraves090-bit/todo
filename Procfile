release: python manage.py migrate --noinput && python manage.py create_admin --username admin --email admin@todoapp.com --password changeme123
web: gunicorn todoapp.wsgi:application --bind 0.0.0.0:$PORT
