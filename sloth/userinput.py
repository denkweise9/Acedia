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
import arrow


class ConversionFailed(Exception):
    def __init__(self, message):
        self.failure_message = message


class Prompter(object):
    """
    A Prompter is an object with a `prompt` method that asks the user
    for input, attempts to convert the value to something useful to
    the application, and if the conversion fails, re-prompt the user.


    A converter is a callable that takes a single string argument and
    returns a validated value of the proper type needed by the
    application, or raises `ConversionFailed` with a message suitable
    to display to the user.

    Extra kwargs passed to the constructor will be used to format the
    prompt and passed into the converter.
    """
    def __init__(self, prompt_text_format, converter, **kwargs):
        prompt_text = prompt_text_format.format(**kwargs)
        self.prompt_text = '{0}: '.format(prompt_text)
        self.convert = converter
        self.convert_kwargs = kwargs
        self.running = True

    def prompt(self, _print=print):
        while True:
            raw_value = input(self.prompt_text)
            try:
                value = self.convert(raw_value, **self.convert_kwargs)
            except ConversionFailed as e:
                _print(e.failure_message)
                if not self.running:
                    break
            else:
                return value


def prompter_from_converter(prompt_text):
    """
    Returns a function that turns a converter callable into a
    `Prompter` instance. Intended to be used as a decorator.
    """
    def decorator(converter):
        return Prompter(prompt_text, converter)
    return decorator


def integer_converter(value):
    try:
        return int(value)
    except ValueError:
        raise ConversionFailed('Please enter a whole number')


@prompter_from_converter(
    'Enter your first name (20 character limit)'
)
def first_name_prompter(raw_value):
    name = raw_value.capitalize().strip()
    if len(name) > 20:
        raise ConversionFailed('There\'s a 20 character limit...')
    if len(name) == 0:
        raise ConversionFailed('How were you expecting that to work?')
    return name


@prompter_from_converter(
    'Enter your birthday (like 1999-12-31)'
)
def age_prompter(raw_value):
    age = raw_value.strip()
    try:
        arrow.Arrow.strptime(age, '%Y-%m-%d').date()
    except ValueError:
        raise ConversionFailed('Format is 1999-12-31')
    return age


@prompter_from_converter('Enter your sex (M/F)')
def sex_prompter(raw_value):
    sex = raw_value.strip().upper()
    if sex != 'M' and sex != 'F':
        raise ConversionFailed('You didn\'t choose male or female.')
    return sex.upper()


@prompter_from_converter(
    'What is your fitness goal?\n'
    '1 for power lifting\n'
    '2 for strength\n'
    '3 for weight loss\n'
    '4 for cardio'
)
def goal_prompter(raw_value):
    goal = integer_converter(raw_value)
    if goal not in [1, 2, 3, 4]:
        raise ConversionFailed('Options are: 1/2/3/4')
    return goal


@prompter_from_converter('(I)mperial or (M)etric measurements?')
def measurement_system_prompter(raw_value):
    system = raw_value.strip().upper()
    if system == ('M'):
        return 'M'
    elif system == ('I'):
        return 'I'
    else:
        raise ConversionFailed('Choose (M)etric or (I)mperial')


@prompter_from_converter('Enter weight in kilograms (float number)')
def metric_body_weight_prompter(raw_value):
    try:
        weight = float(raw_value)
        if weight <= 22.679:
            raise ConversionFailed('Pretty sure that\'s not your real weight.')
        elif weight >= 453.592:
            raise ConversionFailed('I seriously doubt you\'re that big.')
        else:
            return weight
    except ValueError:
        raise ConversionFailed('You can only put in a float (1.0) number.')


@prompter_from_converter('Enter height in meters (float number)')
def metric_body_height_prompter(raw_value):
    try:
        height = float(raw_value)
        if height <= 0.5:
            raise ConversionFailed('Put in your real height, please.')
        elif height >= 2.7:
            raise ConversionFailed('Taller than the tallest person recorded?')
        else:
            return height
    except ValueError:
        raise ConversionFailed('You can only put in a float (1.0) number.')


@prompter_from_converter('Enter weight in pounds (whole number)')
def imperial_body_weight_prompter(raw_value):
    try:
        weight = int(raw_value)
        if weight <= 50:
            raise ConversionFailed('Pretty sure that\'s not your real weight.')
        elif weight >= 1000:
            raise ConversionFailed('I seriously doubt you\'re that big.')
        else:
            return weight
    except ValueError:
        raise ConversionFailed('You can only use whole numbers.')


@prompter_from_converter('Enter height in inches (whole number)')
def imperial_body_height_prompter(raw_value):
    try:
        height = int(raw_value)
        if height <= 20:
            raise ConversionFailed('Put in your real height, please.')
        elif height >= 108:
            raise ConversionFailed('Taller than the tallest person recorded?')
        else:
            return height
    except ValueError:
        raise ConversionFailed('You can only use whole numbers.')


@prompter_from_converter('Do you have anything to log before deterioration? (Y/N)')
def start_log_prompter(raw_value):
    try:
        start_log = raw_value.strip().lower()
        if start_log in ['y', 'yes']:
            return True
        elif start_log in ['', 'n', 'no']:
            return False
        else:
            raise ConversionFailed(
                'That wasn\'t a valid input, let\'s try again.'
            )
    except ValueError:
        raise ConversionFailed('That wasn\'t a valid input, let\'s try again.')


def cardio_date_prompter():
    return Prompter(
        'What day? (Format 1999-12-31) (Enter for today)', cardio_date_converter)


def cardio_date_converter(raw_value):
    try:
        initial_check_date = arrow.Arrow.strptime(raw_value.strip(),
                                                  '%Y-%m-%d')
        check_date_strftime = arrow.Arrow.strptime(initial_check_date, '%Y-%m-%d')
        return check_date_strftime
    except ValueError:
        if raw_value.strip() == '':
            return arrow.Arrow.strftime(arrow.now(), '%Y-%m-%d')
        else:
            raise ConversionFailed('Format is 1999-12-31')    


def cardio_when_prompter():
    return Prompter(
        'What time did you finish? (Format 20:30:15) (Enter for now)', cardio_when_converter
    )


def cardio_when_converter(raw_value):
    time_input = raw_value.strip()
    time_split = time_input.split(':')
    try:
        if len(time_split) == 3:
            hours_ = int(time_split[0])
            minutes_ = int(time_split[1])
            seconds_ = int(time_split[2])
            when_seconds = hours_ * 3600 + minutes_ * 60 + seconds_
            if when_seconds <= 86399:
                log_divmod = divmod(when_seconds, 60)
                when_hours = round(log_divmod[0] / 60)
                when_minutes = round(log_divmod[0] % 60)
                when_seconds = round(log_divmod[1])
                when_time = ('{0:02d}, {1:02d}, {2:02d}'.format(when_hours,
                                                                when_minutes,
                                                                when_seconds))
                return when_time
            else:
                raise ConversionFailed('There\'s only 24 hours in a day')
        elif time_input == '':
            current_time = arrow.now().time()
            when_hours = current_time.hour
            when_minutes = current_time.minute
            when_seconds = current_time.second
            when_time = ('{0:02d} {1:02d} {2:02d}'.format(when_hours,
                                                          when_minutes,
                                                          when_seconds))
            return when_time
        else:
            raise ValueError
    except ValueError:
        raise ConversionFailed(
            'Only digits and ":" can be used. (10:00:00)'
        )


def cardio_time_prompter():
    return Prompter(
        'How long did you go? (10:00/10:00:00)', cardio_time_converter)


def cardio_time_converter(raw_value):
    time_input = raw_value.strip()
    time_split = time_input.split(':')
    try:
        if len(time_split) == 2:
            hours_ = 0
            minutes_ = int(time_split[0])
            seconds_ = int(time_split[1])
        elif len(time_split) == 3:
            hours_ = int(time_split[0])
            minutes_ = int(time_split[1])
            seconds_ = int(time_split[2])
        else:
            raise ValueError
        time_strp = hours_ * 3600 + minutes_ * 60 + seconds_
        if time_strp <= 86399:
            return time_strp
        else:
            raise ConversionFailed('You can\'t put 24 hours+ as your time.')
    except ValueError:
        raise ConversionFailed(
            'Only digits and ":" can be used. (10:00:00/10:00)'
        )


def cardio_distance_imperial_prompter():
    return Prompter(
        'How many miles? (mi to km is 1.609344)',
        cardio_distance_imperial_converter)


def cardio_distance_imperial_converter(raw_value):
    try:
        distance = float(raw_value)
    except (ValueError):
        raise ConversionFailed(
            'A whole ( 1 ) or float ( 1.0 ) number is required'
        )
    if distance >= 50.0:
        raise ConversionFailed(
            'Pretty sure you didn\'t go that far.'
        )
    return distance


def cardio_distance_metric_prompter():
    return Prompter(
        'How many kilometers? (km to mi is 0.62137)',
        cardio_distance_metric_converter)


def cardio_distance_metric_converter(raw_value):
    try:
        distance = float(raw_value)
    except (ValueError):
        raise ConversionFailed(
            'A whole ( 1 ) or float ( 1.0 ) number is required'
        )
    if distance >= 80.467354394322222:
        raise ConversionFailed(
            'Pretty sure you didn\'t go that far.'
        )
    return distance


def stats_agi_prompter(activity):
    activity = 26 - sum(activity)
    return Prompter(
        'Agility - Your reaction time (0/10) ({} left)'.format(activity),
        stats_agi_converter, activity=activity
    )


def stats_agi_converter(raw_value, activity):
    agility = raw_value.strip().lower()
    try:
        if 0 <= int(agility) <= 10:
            agility = int(agility)
            return agility, 1
        elif int(agility) > 10:
            raise ConversionFailed('That\'s over the allowed amount (10)')
    except ValueError:
        raise ConversionFailed('Incorrect input')


def stats_chr_prompter(activity):
    activity = 26 - sum(activity)
    return Prompter(
        'Charisma - Influence over others ({} left)'.format(activity),
        stats_chr_converter, activity=activity
    )


def stats_chr_converter(raw_value, activity):
    charisma = raw_value.strip().lower()
    try:
        if charisma == 'b':
            return 0, 0
        elif 0 <= int(charisma) <= 10:
            charisma = int(charisma)
            return charisma, 2
        elif int(charisma) > 10:
            raise ConversionFailed('That\'s over the allowed amount (10)')
    except ValueError:
        raise ConversionFailed('Incorrect input')


def stats_def_prompter(activity):
    activity = 26 - sum(activity)
    return Prompter(
        'Defense - How well you can take a punch ({} left)'.format(activity),
        stats_def_converter, activity=activity
    )


def stats_def_converter(raw_value, activity):
    defense = raw_value.strip().lower()
    try:
        if defense == 'b':
            return 0, 1
        elif 0 <= int(defense) <= 10:
            if activity - int(defense) <= 0:
                raise ConversionFailed('You have no more points to use..')
            else:
                defense = int(defense)
                return defense, 3
        elif int(defense) > 10:
            raise ConversionFailed('That\'s over the allowed amount (10)')
    except ValueError:
        raise ConversionFailed('Incorrect input')


def stats_end_prompter(activity):
    activity = 26 - sum(activity)
    return Prompter(
        'Endurance - Your overall health ({} left)'.format(activity),
        stats_end_converter, activity=activity
    )


def stats_end_converter(raw_value, activity):
    endurance = raw_value.strip().lower()
    try:
        if endurance == 'b':
            return 0, 2
        elif 0 <= int(endurance) <= 10:
            if activity - int(endurance) <= 0:
                raise ConversionFailed('You have no more points to use..')
            else:
                endurance = int(endurance)
                return endurance, 4
        elif int(endurance) > 10:
            raise ConversionFailed('That\'s over the allowed amount (10)')
    except ValueError:
        raise ConversionFailed('Incorrect input')


def stats_int_prompter(activity):
    activity = 26 - sum(activity)
    return Prompter(
        'Intelligence - Technical know-how ({} left)'.format(activity),
        stats_int_converter, activity=activity
    )


def stats_int_converter(raw_value, activity):
    intelligence = raw_value.strip().lower()
    try:
        if intelligence == 'b':
            return 0, 3
        elif 0 <= int(intelligence) <= 10:
            if activity - int(intelligence) <= 0:
                raise ConversionFailed('You have no more points to use..')
            else:
                intelligence = int(intelligence)
                return intelligence, 5
        elif int(intelligence) > 10:
            raise ConversionFailed('That\'s over the allowed amount (10)')
    except ValueError:
        raise ConversionFailed('Incorrect input')


def stats_str_prompter(activity):
    activity = 26 - sum(activity)
    return Prompter(
        'Strength - How well you can give a punch ({} left)'.format(activity),
        stats_str_converter, activity=activity
    )


def stats_str_converter(raw_value, activity):
    strength = raw_value.strip().lower()
    try:
        if strength == 'b':
            return 0, 4
        elif 0 <= int(strength) <= 10:
            if activity - int(strength) > 0:
                raise ConversionFailed('You still have points to apply.')
            elif activity - int(strength) == 0:
                strength = int(strength)
                return strength, 6
            elif activity - int(strength) < 0:
                raise ConversionFailed('You have no more points to use..')
        elif int(strength) > 10:
            raise ConversionFailed('That\'s over the allowed amount (10).')
    except ValueError:
        raise ConversionFailed('Incorrect input')


def measurement_change_prompter(activity):
    return Prompter(
        'Would you like to switch to {0}? (Y/N)'.format(activity),
        measurement_change_converter, activity=activity
    )


def measurement_change_converter(raw_value, activity):
    measurement = raw_value.strip().lower()
    if measurement.upper() in ['Y', 'YES']:
        return True
    elif measurement.upper() in ['N', 'NO']:
        return False
    else:
        print('I\'ll take that as a no.')
        return False
