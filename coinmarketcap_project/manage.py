#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import atexit


def cleanup_function():
    # This function will run before the Django application is closed abruptly
    print("Cleaning up...")
    
    from coinmarketcap_app.tasks import scraper
    scraper.closeDriver()
    print("WebDriver Closed")

atexit.register(cleanup_function)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coinmarketcap_project.settings')
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
