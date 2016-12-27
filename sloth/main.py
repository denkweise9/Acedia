# Copyright 2015, 2016 Scott King
#
# This file is part of Acedia.
#
# Acedia is free software: you can redistribute it and/or modify
# it under the terms of the Affero GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Acedia is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Affero GNU General Public License for more details.
#
# You should have received a copy of the Affero GNU General Public License
# along with Acedia.  If not, see <http://www.gnu.org/licenses/>.
#
# Autocomplete taken from
# https://stackoverflow.com/questions/7821661/how-to-code-autocompletion-in-python
#

import arrow
import bisect
import os
import readline
import sys
from dateutil.relativedelta import relativedelta
from sloth import userinput
from sloth.store import LogEntry
from sloth.store import LogsStore

# User dir
main_dir = os.path.expanduser("~")

# Quests, Monsters, People, etc are all stored in here
logs_path = os.path.join(main_dir, 'log.ini')

selection = ['A', 'B', 'C']

def initial_questions(settings):
    """
    Settings file will be overwritten if all the data is gathered from
    the user successfully.
    """

    name = userinput.first_name_prompter.prompt()

    initial_stats(settings, name, sex)


def initial_stats(settings, name, sex):

    print('You have 26 points to place into 6 stats.')
    print('Press \'b\' to go back after agility')

    # This is to ensure that the "back" functionality works
    back = 0
    agility = charisma = defense = endurance = intelligence = strength = 0
    while back != 6:
        all_stats = [agility, charisma, defense,
                     endurance, intelligence, strength]
        if back == 0:
            all_stats[0] = 0
            agi_prompter = userinput.stats_agi_prompter(activity=all_stats)
            agility, back = agi_prompter.prompt()
        elif back == 1:
            all_stats[1] = 0
            chr_prompter = userinput.stats_chr_prompter(activity=all_stats)
            charisma, back = chr_prompter.prompt()
        elif back == 2:
            all_stats[2] = 0
            def_prompter = userinput.stats_def_prompter(activity=all_stats)
            defense, back = def_prompter.prompt()
        elif back == 3:
            all_stats[3] = 0
            end_prompter = userinput.stats_end_prompter(activity=all_stats)
            endurance, back = end_prompter.prompt()
        elif back == 4:
            all_stats[4] = 0
            int_prompter = userinput.stats_int_prompter(activity=all_stats)
            intelligence, back = int_prompter.prompt()
        elif back == 5:
            str_prompter = userinput.stats_str_prompter(activity=all_stats)
            strength, back = str_prompter.prompt()
        elif back == 6:
            break
        else:
            raise Exception('Unexpected "back" variable {0!r}'.format(back))

    settings.agility = agility
    settings.charisma = charisma
    settings.defense = defense
    settings.endurance = endurance
    settings.intelligence = intelligence
    settings.strength = strength
    settings.name = name.capitalize()
    settings.age = age
    settings.sex = sex.upper()
    settings.xp = 0

    settings.commit()

# Custom completer
class MyCompleter(object):

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        # on first trigger, build possible matches
        if state == 0:
            # cache matches (entries that start with entered text)
            if text:
                self.matches = [s for s in self.options
                                if s and s.startswith(text.capitalize())]
            # no text entered, all matches possible
            else:
                self.matches = self.options[:]
        try:
            # return match indexed by state
            return self.matches[state]
        except IndexError:
            return None


def personal_checks(settings):

    logs = LogsStore(logs_path)
    personal_checks(logs, settings)


def personal_checks(logs, settings):

    if settings.sex not in ['F', 'M']:
        raise Exception("You're neither female or male?")

    # make sure the stats total up to 26
    stat_list = [settings.agility, settings.charisma, settings.defense,
                 settings.endurance, settings.intelligence,
                 settings.strength]
    if sum(stat_list) != 26:
        raise Exception('Your stats are corrupted.')

    # if log xp and settings.xp don't match, take the xp from the logs
    check_xp(logs, settings)

    total_xp = int(settings.xp)

    level_ = level(total_xp)

    # the only way this would happen is if you messed with the log :-(
    if total_xp < 0:
        raise Exception('Something is wrong with your log file.')
    # impressive, but not yet supported
    elif total_xp > 99749:
        raise Exception('XP that high ({0}) isn't supported... yet.'.format(total_xp))

    hello(settings, logs, total_xp, level_)


def hello(settings, logs, total_xp, level_):

    print('{0}/{1}'.format(
           settings.name,
           settings.sex))

    print('Lvl {0}/XP {1}'.format(level_, total_xp))

press_start(settings, logs)

def press_start(settings, logs):
    completer = MyCompleter([str(k) for k in workouts])
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')

    while True:
        # because windows has to be special
        if sys.platform.startswith('win'):
            choose_extra = "(Tab for options)"
        else:
            choose_extra = "(Double tab for options)"
        choose_ = input('What did you want to do? {0}: '.format(choose_extra))
        if choose_.capitalize() not in selection:
            pass
        else:
            if choose_.capitalize() == 'A':
                print('This is a filler message for now.')
            elif choose_.capitalize() == 'B':
                print('This is a filler message for now.')
            elif choose_.capitalize() == 'Settings':
                print('This is a filler message for now.')
            else:
                print('This is a filler message for now.')
            personal_checks(settings, start_log)


def check_xp(logs, settings):
    logpoints = logs.check_log()

    if logpoints is None:
        if settings.xp != 0:
            settings.xp = 0
            settings.commit()
        return
    else:
        total_points, losing_points = logpoints
        log_total = sum(total_points) - sum(losing_points)

    if settings.xp == log_total:
        pass
    else:
        settings.xp = log_total
        settings.commit()


def level(total_xp):
    breakpoints = [250, 500, 2000, 3750, 5750, 8250, 11000, 14250, 17750,
                   21750, 26000, 30750, 35750, 41250, 47000, 53250, 59750,
                   66750, 74000, 82250, 90750]
    i = bisect.bisect(breakpoints, total_xp)
    return i + 1
