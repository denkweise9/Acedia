#!/usr/bin/env python3
# Copyright 2015, 2016 Scott King
#
# This file is part of Sloth.
#
# Sloth is free software: you can redistribute it and/or modify
# it under the terms of the Affero GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sloth is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Affero GNU General Public License for more details.
#
# You should have received a copy of the Affero GNU General Public License
# along with Sloth.  If not, see <http://www.gnu.org/licenses/>.
#
import os
import sys
from sloth import main
from sloth.store import SettingsStore

# User dir
main_dir = os.path.expanduser("~")

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
                # This is as early as we can set the deterioration question.
                # This way it's only asked ONCE when you start the program.
                start_log = None
                main.body_checks(settings, start_log)
            except ValueError:
                main.initial_questions(settings)
        else:
            # If not, gather the settings
            main.initial_questions(settings)
    except (EOFError, KeyboardInterrupt):
        print('\nGoodbye!')

if __name__ == "__main__":
    run()
