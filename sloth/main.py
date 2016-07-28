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
# Autocomplete taken from
# https://stackoverflow.com/questions/7821661/how-to-code-autocompletion-in-python
#

import arrow
import bisect
import os
import readline
import sys
from dateutil.relativedelta import relativedelta
from sloth import cardio
from sloth import physical
from sloth import userinput
from sloth.store import LogEntry
from sloth.store import LogsStore
from sloth.workouts import workouts

# User dir
main_dir = os.path.expanduser("~") 

# Saved exercises
logs_path = os.path.join(main_dir, 'log.ini')


def initial_questions(settings):
    """
    Settings file will be overwritten if all the data is gathered from
    the user successfully.
    """

    name = userinput.first_name_prompter.prompt()
    age = userinput.age_prompter.prompt()
    sex = userinput.sex_prompter.prompt()
    measurement_system = userinput.measurement_system_prompter.prompt()

    if measurement_system == 'M':
        weight = userinput.metric_body_weight_prompter.prompt()
        height = userinput.metric_body_height_prompter.prompt()
    elif measurement_system == 'I':
        weight = userinput.imperial_body_weight_prompter.prompt()
        height = userinput.imperial_body_height_prompter.prompt()

    goal = userinput.goal_prompter.prompt()

    initial_stats(settings, name, age, sex, measurement_system, weight,
                  height, goal)


def initial_stats(settings, name, age, sex, measurement_system, weight,
                  height, goal):

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
    settings.measuring_type = measurement_system
    settings.weight = weight
    settings.height = height
    settings.goal = goal
    settings.xp = 0

    settings.commit()

    body_checks(settings)


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


def body_checks(settings):

    # check if imperial
    if settings.measuring_type == 'I':
        # height_format = '''{0:.0f}'{1:.0f}"'''.format(
        #                    *divmod(int(settings.height), 12))
        bmi = round((settings.weight / settings.height ** 2) * 703.0, 2)
        if not 50 < settings.weight < 1000:
            raise Exception("Pretty sure {}'s not your real weight.".format(
                             settings.weight))

    # check if metric
    elif settings.measuring_type == 'M':
        # height_format = '''{0}m'''.format(settings.height)
        bmi = round(settings.weight / (settings.height ** 2), 2)
        if not 22.679 < settings.weight < 453.592:
            raise Exception("Pretty sure {}'s not your real weight.".format(
                             settings.weight))
    # type isn't imperial or metric
    else:
        raise Exception('Unexpected units type {0!r}'.format(
                         settings.measuring_type))

    logs = LogsStore(logs_path)

    personal_checks(bmi, logs, settings)


def personal_checks(bmi, logs, settings):

    if settings.sex not in ['F', 'M']:
        raise Exception("You're neither female or male?")

    # make sure the stats total up to 26
    stat_list = [settings.agility, settings.charisma, settings.defense,
                 settings.endurance, settings.intelligence,
                 settings.strength]
    if sum(stat_list) != 26:
        raise Exception('Stat points do not equal 26.')

    if settings.goal not in [1, 2, 3, 4]:
        raise Exception('Unexpected goal ID {0!r}'.format(settings.goal))
    else:
        pass

    bday_ = settings.age.split('-')
    # [0] is year, [1] is month, [2] is day.
    year_, month_, day_ = [int(i) for i in bday_]

    try:
        birthday = arrow.get(year_, month_, day_)
    except ValueError:
        raise Exception('The birthday in your settings file is not possible.')

    birthday_total = relativedelta(arrow.now().naive, birthday.naive)
    current_age = birthday_total.years

    # if log xp and settings.xp don't match, take the xp from the logs
    check_xp(logs, settings)

    total_xp = int(settings.xp)

    level_ = level(total_xp)

    # the only way this would happen is if only a DETERIORATE was in your log
    if total_xp < 0:
        raise Exception('Something is wrong with your log file.')
    # impressive, but not yet supported
    elif total_xp > 99749:
        raise Exception('XP is over 99749')

    hello(settings, logs, birthday_total, current_age, total_xp, level_)


def hello(settings, logs, birthday_total, current_age, total_xp, level_):

    # there are no days, and only years meaning it's YOUR BIRTHDAY, WOO!
    if birthday_total.days == 0 and birthday_total.months == 0:
        birthday_today = ' (HAPPY BIRTHDAY!)'
    else:
        birthday_today = ''
    print('{0}/{1}/{2}{3}'.format(
           settings.name,
           settings.sex,
           current_age,
           birthday_today))

    print('Lvl {0}/XP {1}'.format(level_, total_xp))

    start_log = userinput.start_log_prompter.prompt()
    if not start_log:
        # don't log for 7, 14, 21 days? you'll lose 20% for each 7 days.
        deteriorate(settings, logs)
        log_exercise()
    else:
        log_exercise()

    completer = MyCompleter([str(k) for k in workouts])
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')

    def log_exercise(settings, logs):
        while True:
            # because windows has to be special
            if sys.platform.startswith('win'):
                choose_extra = "(Tab for options)"
            else:
                choose_extra = "(Double tab for options)"
            choose_ = input('What workout did you do? {0}: '.format(choose_extra))
            if choose_.capitalize() not in workouts.keys():
                pass
            else:
                if choose_.capitalize() == 'Cardio':
                    cardio.main(settings, logs)
                elif choose_.capitalize() == 'Log':
                    print("Not yet done")
                elif choose_.capitalize() == 'Settings':
                    settings_change(settings)
                else:
                    physical.main(choose_, settings)
                body_checks(settings)

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


def deteriorate(settings, logs):
    last_entry = logs.load_last_entry()
    if last_entry is None:
        return

    last_utc = last_entry.utc
    utc_to_arrow = arrow.get(last_utc)
    today = arrow.now()
    deteriorate = today - utc_to_arrow
    multiple_remove = int(deteriorate.days / 7)

    if multiple_remove >= 1 and settings.xp * 0.8 > 199.20000000000002:
        previous_xp = settings.xp
        utcnow = arrow.utcnow().timestamp
        for each in range(multiple_remove):
            total_xp = int(settings.xp)
            if total_xp >= 199.20000000000002:
                total_lost = round(total_xp * 0.2)
                settings.xp = round(total_xp * 0.8)

                deter_entry = LogEntry()

                deter_entry.average = 0
                deter_entry.distance = 0
                deter_entry.exercise = "DETERIORATE"
                deter_entry.measuring = settings.measuring_type
                deter_entry.points = 0
                deter_entry.total = total_lost
                deter_entry.utc = utcnow

                logs.append_entry(deter_entry)
                settings.commit()
        xp_lost = previous_xp - settings.xp
        print('Due to not logging anything for {0} days...'.format(
               deteriorate.days))
        print('You\'ve lost {0} XP. Your XP is now {1}'.format(
               xp_lost, settings.xp))


def settings_change(settings):
    if settings.measuring_type == "I":
        other_measuring_type = "M"
        current_measurement = "imperial"
        other_measurement = "metric"
    else:
        other_measuring_type = "I"
        current_measurement = "metric"
        other_measurement = "imperial"

    print("You are currently using {0} for measurment.".format(
           current_measurement))

    change_measurement_prompter = userinput.measurement_change_prompter(
                                  activity=other_measurement)
    change_measurement = change_measurement_prompter.prompt()

    # The international pound is exactly 0.45359237 kilograms
    # A meter is 39.3700787 inches
    if change_measurement:
        if settings.measuring_type == "I":
            settings.height = settings.height / 39.37007874
            settings.weight = settings.weight * 0.45359237
        elif settings.measuring_type == "M":
            settings.height = int(settings.height * 39.37007874)
            settings.weight = int(settings.weight / 0.45359237)
        settings.measuring_type = other_measuring_type
        settings.commit()
    else:
        pass
