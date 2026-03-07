#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skill_recommendation.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# Gemini API Key
GEMINI_API_KEY=AIzaSyD0T6xZCHwIg2gSojQG7NjZeN44Qcz8Il0

# Database settings (if using PostgreSQL)
DB_NAME=skill_recommendation_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# Django settings
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here