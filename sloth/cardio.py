#!/usr/bin/env python3

import bisect
import datetime
from sloth import userinput
from sloth.store import LogEntry
from sloth.workouts import cardio_xplier_dict
from sloth.workouts import workouts


def main(choose_, settings, logs):

    distance = distance_info(settings)

    time_prompter = userinput.cardio_time_prompter(activity=None)
    time_strp = time_prompter.prompt()

    today = datetime.date.today()

    (avg_metric, imperial_hour, imperial_minute, imperial_second,
     metric_hour, metric_minute, metric_second) = average_time(settings,
                                                               time_strp,
                                                               distance)

    # The only time this would happen
    # is if you said you could run a mile faster than 3:43
    # This was previously set to "False",
    # but that means it would be triggered if the seconds were 00
    if imperial_second == -1:
        return

    imperial_minute, imperial_second, total_avg = average_log(avg_metric,
                                                              imperial_hour,
                                                              imperial_minute,
                                                              imperial_second,
                                                              metric_hour,
                                                              metric_minute,
                                                              metric_second)

    log_hours, log_minutes, log_seconds, logging_time = log_time(time_strp)

    base_points, kind, m_xplier, s_xplier = did_i_get_points(distance,
                                                             imperial_minute,
                                                             imperial_second,
                                                             logging_time,
                                                             logs,
                                                             settings,
                                                             today,
                                                             total_avg)

    if not base_points:
        return
    else:
        running_points(base_points, distance, kind, logging_time, logs,
                       m_xplier, settings, s_xplier, today, total_avg)


def distance_info(settings):
    if settings.measuring_type == "I":
        distance_prompter = userinput.cardio_distance_imperial_prompter(
            activity=None)
    elif settings.measuring_type == "M":
        distance_prompter = userinput.cardio_distance_metric_prompter(
            activity=None)
    distance = distance_prompter.prompt()
    return distance


def average_time(settings, time_strp, distance):
    if settings.measuring_type == "M":
        avg_imperial = time_strp.total_seconds() / (distance / 1.609344)
        avg_metric = time_strp.total_seconds() / distance
        metric_first_divmod = divmod(avg_metric, 60)

        if metric_first_divmod[0] >= 60:
            metric_second_divmod = divmod(metric_first_divmod[0], 60)
            metric_hour, metric_minute = round(metric_second_divmod)
        else:
            metric_hour = False
            metric_minute = round(metric_first_divmod[0])

        metric_second = round(metric_first_divmod[1])

    elif settings.measuring_type == "I":
        avg_imperial = time_strp.total_seconds() / distance
        avg_metric = metric_hour = metric_minute = metric_second = False

    imperial_first_divmod = divmod(avg_imperial, 60)

    if imperial_first_divmod[0] >= 60:
        imperial_second_divmod = divmod(imperial_first_divmod[0], 60)
        imperial_hour = round(imperial_second_divmod[0])
        imperial_minute = round(imperial_second_divmod[1])
    else:
        imperial_hour = False
        imperial_minute = round(imperial_first_divmod[0])
    imperial_second = round(imperial_first_divmod[1])

    if not imperial_hour and imperial_minute <= 3 and imperial_second <= 42:
        # this is the only time imperial_second = -1
        # fails the check, and gets kicked back into main()
        imperial_second = -1
        print("You can run faster than Hicham El Guerrouj?")
        print("-" * 28)
    return (avg_metric, imperial_hour, imperial_minute, imperial_second,
            metric_hour, metric_minute, metric_second)


def average_log(avg_metric, imperial_hour, imperial_minute, imperial_second,
                metric_hour, metric_minute, metric_second):
    try:
        if avg_metric:
            if metric_hour:
                total_avg = "{0:02d}:{1:02d}:{2:02d}".format(
                    metric_hour, metric_minute, metric_second)
            else:
                total_avg = "{0:02d}:{1:02d}".format(
                    metric_minute, metric_second)
        else:
            raise ValueError
    except ValueError:
        if imperial_hour:
            total_avg = "{0:02d}:{1:02d}:{2:02d}".format(imperial_hour,
                                                         imperial_minute,
                                                         imperial_second)
        else:
            total_avg = "{0:02d}:{1:02d}".format(
                imperial_minute, imperial_second)
    print("Your average time was {0}".format(total_avg))
    return(imperial_minute, imperial_second, total_avg)


def log_time(time_strp):
    log_divmod = divmod(time_strp.total_seconds(), 60)

    if time_strp.total_seconds() >= 3600:
        log_hours = round(log_divmod[0] / 60)
        log_minutes = round(log_divmod[0] % 60)
        log_seconds = round(log_divmod[1])
        logging_time = ("{0:02d}:{1:02d}:{2:02d}".format(
            log_hours, log_minutes, log_seconds))
    else:
        log_hours = False
        log_minutes = round(log_divmod[0])
        log_seconds = round(log_divmod[1])
        logging_time = ("{0:02d}:{1:02d}".format(
            log_minutes, log_seconds))
    return(log_hours, log_minutes, log_seconds, logging_time)


def did_i_get_points(distance, imperial_minute, imperial_second, logging_time,
                     logs, settings, today, total_avg):
    try:
        if 3 <= imperial_minute <= 18:
            if 3 <= imperial_minute <= 9:
                kind = "Run"
            elif 10 <= imperial_minute <= 14:
                kind = "Jog"
            elif 15 <= imperial_minute <= 18:
                kind = "Walk"
            base_points = workouts["Cardio"][kind]
            m_xplier = cardio_xplier_dict[kind][imperial_minute]
            s_xplier = second_multiplier(imperial_second)
        else:
            kind = "Walk"
            raise KeyError

    # KeyError is only raised if the average minute is greater than 18
    # or less than 3 ( which, the 3:42 check would take care of that )
    except KeyError:
        print("Didn't qualify for points")
        print("-" * 28)
        log_entry = LogEntry()
        log_entry.average = total_avg
        log_entry.date = today.strftime("%B %d, %Y")
        log_entry.distance = distance
        log_entry.exercise = kind.upper()
        log_entry.measuring = settings.measuring_type
        log_entry.points = 0
        log_entry.total = logging_time
        logs.append_entry(log_entry)
        base_points = False
        # kind, and the xpliers aren't calculated if you were too slow
        # so since we have to return something, set them to False!
        # base_points = False to ensure running_points isn't executed
        return (False, False, False, False)
    else:
        return (base_points, kind, m_xplier, s_xplier)


def second_multiplier(avg_second):
    breakpoints = [15, 30, 45, 60]
    s_xpliers = [0.2, 0.15, 0.10, 0.05]
    i = bisect.bisect(breakpoints, avg_second)
    return(s_xpliers[i])


def running_points(base_points, distance, kind, logging_time, logs, m_xplier,
                   settings, s_xplier, today, total_avg):

    if settings.measuring_type == "I":
        total_points = round((base_points * distance) * (m_xplier + s_xplier))
    elif settings.measuring_type == "M":
        total_points = round(base_points * (distance * 0.62137) *
                                           (m_xplier + s_xplier))

    print("{} points were received!".format(total_points))
    print("-" * 28)

    log_entry = LogEntry()
    log_entry.average = total_avg
    log_entry.date = today.strftime("%B %d, %Y")
    log_entry.distance = distance
    log_entry.exercise = kind.upper()
    log_entry.measuring = settings.measuring_type
    log_entry.points = total_points
    log_entry.total = logging_time

    logs.append_entry(log_entry)

    settings.xp = settings.xp + total_points
    settings.commit()
