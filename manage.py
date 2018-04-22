#!/usr/bin/env python
import os
import sys
import dotenv

if __name__ == "__main__":
    dotenv.read_dotenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fweather.settings")
    if not 'gmail' in os.environ:
        print('gmail environment variable is empty...')
        print('attempting to read from file...')
        root_dir = os.path.dirname(os.path.abspath(__file__))
        client_file = os.path.join(root_dir, 'client_id.json')
        with open(client_file, 'r') as f:
            os.environ['gmail'] = f.read()
            print('...saved environment variable!')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
