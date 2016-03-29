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
import unittest
from unittest.mock import patch


class BaseConverterTestCase(unittest.TestCase):
    """
    Base class for converter tests. Subclass and override the
    `get_converter` method that returns the converter to use in the
    `assertConversion*` methods.
    """
    def get_converter(self):
        raise NotImplementedError

    def assertConversionFails(self, raw_value, **kwargs):
        """
        Verify the converter raises `ConversionFailed` when called
        with the string value.
        """
        # guard against bad test values
        if type(raw_value) is not str:
            raise TypeError('Expected str, got {0}'.format(type(raw_value)))

        from sloth.userinput import ConversionFailed
        converter = self.get_converter()

        with self.assertRaises(ConversionFailed):
            converter(raw_value, **kwargs)

    def assertConversionResultEquals(self, raw_value, expected_result,
                                     **kwargs):
        """
        Verify the converter does not raise `ConversionFailed` when
        called with the string value, and that the result matches
        `expected_result` and is the same type.
        """
        from sloth.userinput import ConversionFailed
        converter = self.get_converter()

        try:
            result = converter(raw_value, **kwargs)
        except ConversionFailed as e:
            msgfmt = (
                'Raw value {raw_value!r} caused unexpected ConversionFailed '
                'with failure message {e.failure_message!r}'
            )
            raise AssertionError(msgfmt.format(raw_value=raw_value, e=e))

        self.assertEqual(result, expected_result)
        self.assertIs(type(result), type(expected_result))


class PrompterTestCase(BaseConverterTestCase):
    def converter(self, raw_value):
        return raw_value

    def raisesException(*args, **kwargs):
        from sloth.userinput import ConversionFailed
        raise ConversionFailed('ConversionFailed')

    @patch('builtins.input', return_value='passes')
    def test_prompt_exception_works(self, input):
        from sloth.userinput import Prompter
        prompt = Prompter('testing: ', self.raisesException)
        prompt.running = False
        printed = []
        prompt.prompt(_print=printed.append)
        self.assertEqual(printed, ['ConversionFailed'])

    @patch('builtins.input', return_value='passes')
    def test_prompt_works(self, input):
        from sloth.userinput import Prompter
        prompt = Prompter('testing: ', self.converter)
        self.assertEqual(prompt.prompt(), 'passes')

    def test_prompter_works(self):
        from sloth.userinput import Prompter
        text = 'Test'
        prompter = Prompter(text, self.converter)
        self.assertEqual(prompter.prompt_text, 'Test: ')


class IntegerConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import integer_converter
        return integer_converter

    def test_integers_works(self):
        for i in [1, 50, 1234]:
            intstr = str(i)
            self.assertConversionResultEquals(intstr, i)

    def test_nonintegers_fails(self):
        self.assertConversionFails('i am certainly not an int')
        self.assertConversionFails('0xBEEF')


class FirstNameConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        # This shows how we can get the converter from a prompter.
        # This is the reason I don't really like the prompter decorator
        # API, it conflates prompting with validation and conversion.
        # We can do better.
        from sloth.userinput import first_name_prompter
        return first_name_prompter.convert

    def test_leading_and_trailing_whitespace_stripped_works(self):
        self.assertConversionResultEquals('  myname  ', 'Myname')

    def test_normal_name_works(self):
        self.assertConversionResultEquals('a', 'A')
        self.assertConversionResultEquals('alice', 'Alice')
        self.assertConversionResultEquals('aaaaaa', 'Aaaaaa')

    def test_name_just_spaces_fails(self):
        self.assertConversionFails('')
        self.assertConversionFails(' ')

    def test_name_longer_than_20_fails(self):
        self.assertConversionFails('A' * 21)


class AgeConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import age_prompter
        return age_prompter.convert

    def test_correct_birthday_works(self):
        self.assertConversionResultEquals('1999-12-31', '1999-12-31')

    def test_day_does_not_exist_fails(self):
        self.assertConversionFails('1999-11-31')

    def test_incorrect_format_fails(self):
        self.assertConversionFails('12-31-1999')
        self.assertConversionFails('31-12-1999')

    def test_random_fails(self):
        self.assertConversionFails('lol')


class SexConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import sex_prompter
        return sex_prompter.convert

    def test_male_works(self):
        self.assertConversionResultEquals('m', 'M')
        self.assertConversionResultEquals('M', 'M')

    def test_female_works(self):
        self.assertConversionResultEquals('f', 'F')
        self.assertConversionResultEquals('F', 'F')

    def test_random_fails(self):
        self.assertConversionFails('123')
        self.assertConversionFails('foo')
        self.assertConversionFails('bar')


class GoalConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import goal_prompter
        return goal_prompter.convert

    def test_valid_works(self):
        self.assertConversionResultEquals('1', 1)
        self.assertConversionResultEquals('2', 2)
        self.assertConversionResultEquals('3', 3)
        self.assertConversionResultEquals('4', 4)

    def test_random_fails(self):
        self.assertConversionFails('123')
        self.assertConversionFails('foo')
        self.assertConversionFails('bar')


class MeasurementSystemConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import measurement_system_prompter
        return measurement_system_prompter.convert

    def test_metric_works(self):
        self.assertConversionResultEquals('m', 'M')
        self.assertConversionResultEquals('M', 'M')

    def test_imperial_works(self):
        self.assertConversionResultEquals('i', 'I')
        self.assertConversionResultEquals('I', 'I')

    def test_invalid_fails(self):
        self.assertConversionFails('123')
        self.assertConversionFails('foo')
        self.assertConversionFails('imperial')
        self.assertConversionFails('metric')


class ImperialHeightConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import imperial_body_height_prompter
        return imperial_body_height_prompter.convert

    def test_twenty_and_lower_fails(self):
        self.assertConversionFails('19')
        self.assertConversionFails('20')

    def test_one_hundred_and_eight_and_higher_fails(self):
        self.assertConversionFails('108')
        self.assertConversionFails('109')

    def test_valid_works(self):
        self.assertConversionResultEquals('50', 50)

    def test_invalid_fails(self):
        self.assertConversionFails('a')


class ImperialWeightConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import imperial_body_weight_prompter
        return imperial_body_weight_prompter.convert

    def test_fifty_and_under_fails(self):
        self.assertConversionFails('49')
        self.assertConversionFails('50')

    def test_one_thousand_and_higher_fails(self):
        self.assertConversionFails('1000')
        self.assertConversionFails('1001')

    def test_valid_works(self):
        self.assertConversionResultEquals('200', 200)

    def test_non_float_fails(self):
        self.assertConversionFails('a')


class MetricHeightConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import metric_body_height_prompter
        return metric_body_height_prompter.convert

    def test_zero_point_five_and_lower_fails(self):
        self.assertConversionFails('0.5')
        self.assertConversionFails('0.49')

    def test_two_point_seven_and_higher_fails(self):
        self.assertConversionFails('2.7')
        self.assertConversionFails('2.71')

    def test_valid_works(self):
        self.assertConversionResultEquals('2.0', 2.0)

    def test_non_float_fails(self):
        self.assertConversionFails('a')


class MetricWeightConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import metric_body_weight_prompter
        return metric_body_weight_prompter.convert

    def test_twenty_two_point_six_seven_nine_and_under_fails(self):
        self.assertConversionFails('22.679')
        self.assertConversionFails('22.67')

    def test_four_hundred_fifty_three_point_five_nine_two_and_over_fails(self):
        self.assertConversionFails('453.592')
        self.assertConversionFails('453.6')

    def test_valid_works(self):
        self.assertConversionResultEquals('200', 200.0)

    def test_non_float_fails(self):
        self.assertConversionFails('a')


class CardioTimeConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import cardio_time_converter
        return cardio_time_converter

    def test_prompter_works(self):
        from sloth.userinput import cardio_time_prompter
        activity = None
        prompter = cardio_time_prompter(activity)
        expected = 'How long did you go? (10:00/10:00:00): '
        self.assertEqual(prompter.prompt_text, expected)

    def test_notime_fails(self):
        self.assertConversionFails('not a time')

    def test_minutes_seconds_works(self):
        import datetime
        seconds = 23 * 60 + 45
        seconds_timedelta = datetime.timedelta(0, seconds)
        self.assertConversionResultEquals('23:45', seconds_timedelta)

    def test_hours_minutes_seconds_works(self):
        import datetime
        seconds = 2 * 3600 + 49 * 60 + 34
        seconds_timedelta = datetime.timedelta(0, seconds)
        self.assertConversionResultEquals('02:49:34', seconds_timedelta)

    def test_hours_minutes_seconds_and_more_fails(self):
        self.assertConversionFails('0:1:2:3')
        self.assertConversionFails('0:1:2:3:4')

    def test_24_hours_and_more_fails(self):
        self.assertConversionFails('23:60:00')
        self.assertConversionFails('0:1440:0')
        self.assertConversionFails('0:0:86400')


class CardioDistanceImperialDistanceConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import cardio_distance_imperial_converter
        return cardio_distance_imperial_converter

    def test_prompter_works(self):
        from sloth.userinput import cardio_distance_imperial_prompter
        activity = None
        prompter = cardio_distance_imperial_prompter(activity)
        expected = 'How many miles? (mi to km is 1.609344): '
        self.assertEqual(prompter.prompt_text, expected)

    def test_valid_works(self):
        self.assertConversionResultEquals('10.234', 10.234, activity=None)

    def test_invalid_fails(self):
        self.assertConversionFails('50.1', activity=None)

    def test_ridiculous_fails(self):
        self.assertConversionFails('a', activity=None)


class CardioDistanceMetricDistanceConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import cardio_distance_metric_converter
        return cardio_distance_metric_converter

    def test_prompter_works(self):
        from sloth.userinput import cardio_distance_metric_prompter
        activity = None
        prompter = cardio_distance_metric_prompter(activity)
        expected = 'How many kilometers? (km to mi is 0.62137): '
        self.assertEqual(prompter.prompt_text, expected)

    def test_reasonable_works(self):
        self.assertConversionResultEquals('10.234', 10.234, activity='Run')

    def test_invalid_fails(self):
        self.assertConversionFails('80.4674', activity='Run')

    def test_non_float_fails(self):
        self.assertConversionFails('F', activity='Run')


class AgilityStatTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import stats_agi_converter
        return stats_agi_converter

    def test_prompter_works(self):
        from sloth.userinput import stats_agi_prompter
        activity = [0]
        prompter = stats_agi_prompter(activity)
        expected = 'Agility - Your reaction time (0/10) (26 left): '
        self.assertEqual(prompter.prompt_text, expected)

    def test_reasonable_works(self):
        self.assertConversionResultEquals('1', (1, 1), activity=26)

    def test_over_10_fails(self):
        self.assertConversionFails('11', activity=26)

    def test_value_error_works(self):
        self.assertConversionFails('c', activity=26)


class CharismaStatConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import stats_chr_converter
        return stats_chr_converter

    def test_prompter_works(self):
        from sloth.userinput import stats_chr_prompter
        activity = [0]
        prompter = stats_chr_prompter(activity)
        expected = 'Charisma - Influence over others (26 left): '
        self.assertEqual(prompter.prompt_text, expected)

    def test_reasonable_works(self):
        self.assertConversionResultEquals('1', (1, 2), activity=26)

    def test_back_works(self):
        self.assertConversionResultEquals('b', (0, 0), activity=26)

    def test_over_10_fails(self):
        self.assertConversionFails('12', activity=26)

    def test_value_error_works(self):
        self.assertConversionFails('d', activity=26)


class DefenseTestConverterCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import stats_def_converter
        return stats_def_converter

    def test_prompter_works(self):
        from sloth.userinput import stats_def_prompter
        activity = [20]
        prompter = stats_def_prompter(activity)
        expected = 'Defense - How well you can take a punch (6 left): '
        self.assertEqual(prompter.prompt_text, expected)

    def test_not_enough_works(self):
        self.assertConversionFails('1', activity=0)

    def test_back_works(self):
        self.assertConversionResultEquals('b', (0, 1), activity=26)

    def test_reasonable_works(self):
        self.assertConversionResultEquals('1', (1, 3), activity=26)

    def test_over_10_fails(self):
        self.assertConversionFails('13', activity=26)

    def test_value_error_works(self):
        self.assertConversionFails('e', activity=26)


class EnduranceStatConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import stats_end_converter
        return stats_end_converter

    def test_prompter_works(self):
        from sloth.userinput import stats_end_prompter
        activity = [12]
        prompter = stats_end_prompter(activity)
        expected = 'Endurance - Your overall health (14 left): '
        self.assertEqual(prompter.prompt_text, expected)

    def test_not_enough_works(self):
        self.assertConversionFails('1', activity=0)

    def test_back_works(self):
        self.assertConversionResultEquals('b', (0, 2), activity=26)

    def test_reasonable_works(self):
        self.assertConversionResultEquals('1', (1, 4), activity=26)

    def test_over_10_fails(self):
        self.assertConversionFails('14', activity=26)

    def test_value_error_works(self):
        self.assertConversionFails('f', activity=26)


class IntelligenceStatConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import stats_int_converter
        return stats_int_converter

    def test_prompter_works(self):
        from sloth.userinput import stats_int_prompter
        activity = [8]
        prompter = stats_int_prompter(activity)
        expected = 'Intelligence - Technical know-how (18 left): '
        self.assertEqual(prompter.prompt_text, expected)

    def test_not_enough_works(self):
        self.assertConversionFails('1', activity=0)

    def test_back_works(self):
        self.assertConversionResultEquals('b', (0, 3), activity=26)

    def test_reasonable_works(self):
        self.assertConversionResultEquals('1', (1, 5), activity=26)

    def test_over_10_fails(self):
        self.assertConversionFails('15', activity=26)

    def test_value_error_works(self):
        self.assertConversionFails('g', activity=26)


class StrengthStatConverterTestCase(BaseConverterTestCase):
    def get_converter(self):
        from sloth.userinput import stats_str_converter
        return stats_str_converter

    def test_prompter_works(self):
        from sloth.userinput import stats_str_prompter
        activity = [24]
        prompter = stats_str_prompter(activity)
        expected = 'Strength - How well you can give a punch (2 left): '
        self.assertEqual(prompter.prompt_text, expected)

    def test_not_enough_works(self):
        self.assertConversionFails('1', activity=0)

    def test_back_works(self):
        self.assertConversionResultEquals('b', (0, 4), activity=26)

    def test_reasonable_works(self):
        self.assertConversionResultEquals('1', (1, 6), activity=1)

    def test_points_still_available(self):
        self.assertConversionFails('1', activity=2)

    def test_over_10_fails(self):
        self.assertConversionFails('16', activity=1)

    def test_value_error_works(self):
        self.assertConversionFails('h', activity=26)

    def test_zero_or_less_available_works(self):
        self.assertConversionFails('1', activity=0)
