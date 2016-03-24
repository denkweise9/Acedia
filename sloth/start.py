#!/usr/bin/env python3

import os
import sys
from sloth import main
from sloth.store import SettingsStore

# The directory this program is running from
main_dir = os.getcwd()

# File where all info on user is stored
settings_path = os.path.join(main_dir, 'settings.ini')


def run():
    try:
        if sys.platform.startswith(('cygwin', 'win')):
            try:
                import pyreadline as readline # noqa
            except ImportError:
                print('Please \'pip install pyreadline\' in your virtualenv.')
                sys.exit()

        settings = SettingsStore(settings_path)
        # Check if settings file exists
        if os.path.isfile(settings_path):
            # If it does, start the main program.
            try:
                settings.load()
                main.body_checks(settings)
            except ValueError:
                main.initial_questions(settings)
        else:
            # If not, gather the settings
            main.initial_questions(settings)
    except (EOFError, KeyboardInterrupt):
        print('\nGoodbye!')

if __name__ == "__main__":
    run()
