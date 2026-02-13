#!/bin/bash

# Run migrations
python manage.py migrate --noinput

# Create admin if doesn't exist
python manage.py create_admin --username admin --email admin@todoapp.com --password changeme123

# Collect static files
python manage.py collectstatic --noinput

echo "Setup complete!"
