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
cardio_xplier_dict = {'Run': {9: 0.5, 8: 0.7, 7: 0.9, 6: 1.1, 5: 1.3, 4: 1.5,
                              3: 1.7
                             },
                      'Jog': {18: 0.20, 17: 0.25, 16: 0.3, 15: 0.35, 14: 0.2,
                              13: 0.4, 12: 0.6, 11: 0.8, 10: 0.95
                             },
                      'Walk': {28: 0.05, 27: 0.1, 26: 0.15, 25: 0.2, 24: 0.25,
                               23: 0.3, 22: 0.35, 21: 0.4, 20: 0.45, 19: 0.5
                              }
                     }
workouts = {'Bicycle': 200, 'Bodyweight Squat': 200, 'Burpee': 300,
            'Cardio': {'Jog': 300, 'Run': 400, 'Walk': 100}, 'I': 200,
            'Log': 0, 'Pull-up': 500, 'Push-ups': 200, 'Settings': 0,
            'Sit-up': 200, 'T': 200, 'Y': 200
           }
