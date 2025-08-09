#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'endless_nights.settings')
    
    # Auto-assign unique port 8742 for Endless Nights Engine
    if 'runserver' in sys.argv:
        # Check if port is already specified
        has_port = False
        for arg in sys.argv:
            if ':' in arg or arg.isdigit():
                has_port = True
                break
        if not has_port:
            # Find runserver position and add port after it
            runserver_index = sys.argv.index('runserver')
            sys.argv.insert(runserver_index + 1, '0.0.0.0:8747')
    
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