#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    if os.getenv("VIRTUAL_ENV") is None:  # for development
        try:
            import dotenv
            dotenv.load_dotenv(
                Path(__file__).resolve().parent.parent.parent / ".env")
        except ImportError:
            pass
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "ft_transcendence.settings")
    try:
        # pylint: disable=import-outside-toplevel
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
