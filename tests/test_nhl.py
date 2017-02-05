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

from hockepy import nhl

class TestNhl(unittest.TestCase):
    """Tests for hockepy.nhl module."""

    KNOWN_SCHEDULE = {
        '2014-01-01': [
            nhl.Game(home='Detroit Red Wings', away='Toronto Maple Leafs'),
            nhl.Game(home='Vancouver Canucks', away='Tampa Bay Lightning')
            ],
        '2016-06-01': [
            nhl.Game(home='Pittsburgh Penguins', away='San Jose Sharks')
            ],
        '2016-07-01': [],
        '2017-02-05': [
            nhl.Game(home='New York Rangers', away='Calgary Flames'),
            nhl.Game(home='Montréal Canadiens', away='Edmonton Oilers'),
            nhl.Game(home='Washington Capitals', away='Los Angeles Kings')
            ]
        }

    def test01_get_schedule_known_dates(self):
        """Test that schedule can be retrieved correctly.

        Use dates for which the schedule is known and compare the result
        with expected data.
        """
        for day, games in self.KNOWN_SCHEDULE.items():
            schedule = nhl.get_schedule(day)
            self.assertEqual(len(games), len(schedule))
            for game in schedule:
                self.assertIn(game, games)
