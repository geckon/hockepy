# vim: set fileencoding=utf-8 :

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

import json
import os
import unittest
from datetime import datetime

import requests

from hockepy import nhl


class TestNhl(unittest.TestCase):
    """Tests for hockepy.nhl module."""

    TEST_DATA = 'tests/test_data'

    TIME_FMT = '%Y-%m-%dT%H:%M:%S%z'

    KNOWN_SCHEDULE = {
        '2014-01-01': {'2014-01-01': [
            nhl.Game(home='Detroit Red Wings',
                     away='Toronto Maple Leafs',
                     time=datetime.strptime('2014-01-01T18:00:00+0000',
                                            TIME_FMT),
                     type='R',
                     status='Final'),
            nhl.Game(home='Vancouver Canucks',
                     away='Tampa Bay Lightning',
                     time=datetime.strptime('2014-01-02T03:00:00+0000',
                                            TIME_FMT),
                     type='R',
                     status='Final'),
        ]},
        '2016-06-01': {'2016-06-01': [
            nhl.Game(home='Pittsburgh Penguins',
                     away='San Jose Sharks',
                     time=datetime.strptime('2016-06-02T00:00:00+0000',
                                            TIME_FMT),
                     type='P',
                     status='Final'),
        ]},
        '2016-07-01': None,
        '2017-02-05': {'2017-02-05': [
            nhl.Game(home='New York Rangers',
                     away='Calgary Flames',
                     time=datetime.strptime('2017-02-05T19:00:00+0000',
                                            TIME_FMT),
                     type='R',
                     status='Final'),
            nhl.Game(home='Montréal Canadiens',
                     away='Edmonton Oilers',
                     time=datetime.strptime('2017-02-05T18:00:00+0000',
                                            TIME_FMT),
                     type='R',
                     status='Final'),
            nhl.Game(home='Washington Capitals',
                     away='Los Angeles Kings',
                     time=datetime.strptime('2017-02-05T17:00:00+0000',
                                            TIME_FMT),
                     type='R',
                     status='Final'),
        ]}
    }

    MOCK_SCHEDULE = {
        '2017-07-04': [
            nhl.Game(home='Gotham City Bats',
                     away='Springfield Electrons',
                     time=datetime.strptime('2017-07-04T21:00:00+0000',
                                            TIME_FMT),
                     type='R',
                     status='Final')
        ],
        '2017-07-07': [
            nhl.Game(home='Hill Valley Time Travelers',
                     away='Sin City Sinners',
                     time=datetime.strptime('2017-07-08T00:00:00+0000',
                                            TIME_FMT),
                     type='PR',
                     status='Final'),
            nhl.Game(home='Castle Black Crows',
                     away='Los Santos Gangsters',
                     time=datetime.strptime('2017-07-08T03:00:00+0000',
                                            TIME_FMT),
                     type='R',
                     status='Game Over'),
            nhl.Game(home='Shire Halflings',
                     away='Hogsmeade Wizards',
                     time=datetime.strptime('2017-07-07T20:30:00+0000',
                                            TIME_FMT),
                     type='P',
                     status='In Progress - Critical'),
        ],
        '2017-07-08': [
            nhl.Game(home='Smallville Reporters',
                     away='Albuquerque Meths',
                     time=datetime.strptime('2017-07-09T01:00:00+0000',
                                            TIME_FMT),
                     type='P',
                     status='In Progress'),
            nhl.Game(home='Asgard Gods',
                     away='Hill Valley Time Travelers',
                     time=datetime.strptime('2017-07-08T21:30:00+0000',
                                            TIME_FMT),
                     type='P',
                     status='Pre-Game'),
            nhl.Game(home='Hogsmeade Wizards',
                     away='Gotham City Bats',
                     time=datetime.strptime('2017-07-09T01:30:00+0000',
                                            TIME_FMT),
                     type='P',
                     status='Scheduled'),
        ]
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

    def test03_wrong_date_format(self):
        """Test that get_schedule() fails graciously for wrong dates."""
        with self.assertRaises(requests.exceptions.HTTPError):
            nhl.get_schedule('2017-48-25', '2017-48-25')

    def test04_parse_schedule_mock(self):
        """Test that parse_schedule() returns expected values.

        Instead of hitting NHL API, mock JSON file is parsed here.
        """
        sched_path = os.path.join(self.TEST_DATA, 'nhl_mock_schedule.json')
        with open(sched_path) as schedule_file:
            schedule = nhl.parse_schedule(json.loads(schedule_file.read()))

        self.assertEqual(len(self.MOCK_SCHEDULE), len(schedule))
        for day in self.MOCK_SCHEDULE:
            self.assertEqual(len(self.MOCK_SCHEDULE[day]), len(schedule[day]))
            for game in schedule[day]:
                self.assertIn(game, self.MOCK_SCHEDULE[day])

    def test05_parse_schedule_empty(self):
        """Test that an empty schedule is correctly parsed."""
        sched_path = os.path.join(self.TEST_DATA, 'nhl_empty_schedule.json')
        with open(sched_path) as schedule_file:
            schedule = nhl.parse_schedule(json.loads(schedule_file.read()))
        self.assertEqual(schedule, None)
