#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.nhl module tests
------------------------
"""

import unittest
from time import strptime

from hockepy import nhl


class TestNhl(unittest.TestCase):
    """Tests for hockepy.nhl module."""

    TIME_FMT = '%Y-%m-%dT%H:%M:%SZ'

    KNOWN_SCHEDULE = {
        '2014-01-01': {'2014-01-01': [
            nhl.Game(home='Detroit Red Wings',
                     away='Toronto Maple Leafs',
                     time=strptime('2014-01-01T18:00:00Z', TIME_FMT)),
            nhl.Game(home='Vancouver Canucks',
                     away='Tampa Bay Lightning',
                     time=strptime('2014-01-02T03:00:00Z', TIME_FMT)),
            ]},
        '2016-06-01': {'2016-06-01': [
            nhl.Game(home='Pittsburgh Penguins',
                     away='San Jose Sharks',
                     time=strptime('2016-06-02T00:00:00Z', TIME_FMT)),
            ]},
        '2016-07-01': None,
        '2017-02-05': {'2017-02-05': [
            nhl.Game(home='New York Rangers',
                     away='Calgary Flames',
                     time=strptime('2017-02-05T19:00:00Z', TIME_FMT)),
            nhl.Game(home='Montréal Canadiens',
                     away='Edmonton Oilers',
                     time=strptime('2017-02-05T18:00:00Z', TIME_FMT)),
            nhl.Game(home='Washington Capitals',
                     away='Los Angeles Kings',
                     time=strptime('2017-02-05T17:00:00Z', TIME_FMT)),
            ]}
        }

    NO_SCHEDULE_PERIODS = {
        ('2016-07-01', '2016-07-01'),
        ('2016-07-01', '2016-07-31')
        }

    def test01_get_schedule_known_dates(self):
        """Test that schedule can be retrieved correctly.

        Use dates for which the schedule is known and compare the result
        with expected data.
        """
        for day, day_schedule in self.KNOWN_SCHEDULE.items():
            schedule = nhl.get_schedule(day, day)
            if day_schedule is None:
                self.assertEqual(schedule, None)
            else:
                self.assertEqual(len(day_schedule), len(schedule))
                self.assertEqual(len(day_schedule[day]), len(schedule[day]))
                for game in schedule[day]:
                    self.assertIn(game, day_schedule[day])

    def test02_get_schedule_empty(self):
        """Test that get_schedule() behaves correctly for no games days.

        Use dates that are known for no games played (like off-season)
        and check that get_schedule() returns None as it should.
        """
        for period in self.NO_SCHEDULE_PERIODS:
            schedule = nhl.get_schedule(*period)
            self.assertEqual(schedule, None)
