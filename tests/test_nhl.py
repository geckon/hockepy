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
from hockepy.game import Game, GameStatus, GameType, Play


class TestNhl(unittest.TestCase):
    """Tests for hockepy.nhl module."""

    TEST_DATA = 'tests/test_data'

    TIME_FMT = '%Y-%m-%dT%H:%M:%S%z'

    KNOWN_SCHEDULE = {
        '2014-01-01': {'2014-01-01': [
            Game(home='Detroit Red Wings',
                 away='Toronto Maple Leafs',
                 home_score=2,
                 away_score=3,
                 time=datetime.strptime('2014-01-01T18:00:00+0000', TIME_FMT),
                 type=GameType.REGULAR,
                 status=GameStatus.FINAL,
                 last_play=('SO', '65:00', 'Game End')),
            Game(home='Vancouver Canucks',
                 away='Tampa Bay Lightning',
                 home_score=2,
                 away_score=4,
                 time=datetime.strptime('2014-01-02T03:00:00+0000', TIME_FMT),
                 type=GameType.REGULAR,
                 status=GameStatus.FINAL,
                 last_play=('3rd', '60:00', 'Game End')),
        ]},
        '2016-06-01': {'2016-06-01': [
            Game(home='Pittsburgh Penguins',
                 away='San Jose Sharks',
                 home_score=2,
                 away_score=1,
                 time=datetime.strptime('2016-06-02T00:00:00+0000', TIME_FMT),
                 type=GameType.PLAYOFFS,
                 status=GameStatus.FINAL,
                 last_play=('OT', '62:35', 'Game End')),
        ]},
        '2016-07-01': None,
        '2017-02-05': {'2017-02-05': [
            Game(home='New York Rangers',
                 away='Calgary Flames',
                 home_score=4,
                 away_score=3,
                 time=datetime.strptime('2017-02-05T19:00:00+0000', TIME_FMT),
                 type=GameType.REGULAR,
                 status=GameStatus.FINAL,
                 last_play=('3rd', '60:00', 'Game End')),
            Game(home='Montréal Canadiens',
                 away='Edmonton Oilers',
                 home_score=0,
                 away_score=1,
                 time=datetime.strptime('2017-02-05T18:00:00+0000', TIME_FMT),
                 type=GameType.REGULAR,
                 status=GameStatus.FINAL,
                 last_play=('SO', '65:00', 'Game Official')),
            Game(home='Washington Capitals',
                 away='Los Angeles Kings',
                 home_score=5,
                 away_score=0,
                 time=datetime.strptime('2017-02-05T17:00:00+0000', TIME_FMT),
                 type=GameType.REGULAR,
                 status=GameStatus.FINAL,
                 last_play=('3rd', '60:00', 'Game End')),
        ]}
    }

    MOCK_SCHEDULE = {
        '2017-07-04': [
            Game(home='Gotham City Bats',
                 away='Springfield Electrons',
                 home_score=2,
                 away_score=3,
                 time=datetime.strptime('2017-07-04T21:00:00+0000', TIME_FMT),
                 type=GameType.REGULAR,
                 status=GameStatus.FINAL,
                 last_play=None)
        ],
        '2017-07-07': [
            Game(home='Hill Valley Time Travelers',
                 away='Sin City Sinners',
                 home_score=3,
                 away_score=2,
                 time=datetime.strptime('2017-07-08T00:00:00+0000', TIME_FMT),
                 type=GameType.PRESEASON,
                 status=GameStatus.FINAL,
                 last_play=None),
            Game(home='Castle Black Crows',
                 away='Los Santos Gangsters',
                 home_score=0,
                 away_score=4,
                 time=datetime.strptime('2017-07-08T03:00:00+0000', TIME_FMT),
                 type=GameType.REGULAR,
                 status=GameStatus.FINAL,
                 last_play=None),
            Game(home='Shire Halflings',
                 away='Hogsmeade Wizards',
                 home_score=1,
                 away_score=0,
                 time=datetime.strptime('2017-07-07T20:30:00+0000', TIME_FMT),
                 type=GameType.PLAYOFFS,
                 status=GameStatus.LIVE,
                 last_play=None),
        ],
        '2017-07-08': [
            Game(home='Smallville Reporters',
                 away='Albuquerque Meths',
                 home_score=6,
                 away_score=6,
                 time=datetime.strptime('2017-07-09T01:00:00+0000', TIME_FMT),
                 type=GameType.PLAYOFFS,
                 status=GameStatus.LIVE,
                 last_play=None),
            Game(home='Asgard Gods',
                 away='Hill Valley Time Travelers',
                 home_score=0,
                 away_score=0,
                 time=datetime.strptime('2017-07-08T21:30:00+0000', TIME_FMT),
                 type=GameType.PLAYOFFS,
                 status=GameStatus.SCHEDULED,
                 last_play=None),
            Game(home='Hogsmeade Wizards',
                 away='Gotham City Bats',
                 home_score=0,
                 away_score=0,
                 time=datetime.strptime('2017-07-09T01:30:00+0000', TIME_FMT),
                 type=GameType.PLAYOFFS,
                 status=GameStatus.SCHEDULED,
                 last_play=None),
            Game(home='Shire Halflings',
                 away='Springfield Electrons',
                 home_score=0,
                 away_score=0,
                 time='TBD',
                 type=GameType.PLAYOFFS,
                 status=GameStatus.SCHEDULED,
                 last_play=None),
        ]
    }

    NO_SCHEDULE_PERIODS = {
        ('2016-07-01', '2016-07-01'),
        ('2016-07-01', '2016-07-31')
        }

    # the "no-goal" final PO game's ID (Dallas Stars @ Buffalo Sabres in 1999)
    NO_GOAL_GAME_ID = 1998030416

    NO_GOAL_PLAY_ITSELF = {
        'players': [{
            'player': {
                'id': 8448091,
                'fullName': 'Brett Hull',
                'link': '/api/v1/people/8448091'
            },
            'seasonTotal': 8,
            'playerType': 'Scorer'
        }, {
            'player': {
                'id': 8459024,
                'fullName': 'Jere Lehtinen',
                'link': '/api/v1/people/8459024'
            },
            'seasonTotal': 3,
            'playerType': 'Assist'
        }, {
            'player': {
                'id': 8449645,
                'fullName': 'Mike Modano',
                'link': '/api/v1/people/8449645'
            },
            'seasonTotal': 18,
            'playerType': 'Assist'
        }, {
            'player': {
                'id': 8447687,
                'fullName': 'Dominik Hasek',
                'link': '/api/v1/people/8447687'
            },
            'playerType': 'Goalie'
        }],
        'coordinates': {},
        'result': {
            'strength': {
                'name': 'Even',
                'code': 'EVEN'
            },
            'eventCode': 'BUF6891',
            'gameWinningGoal': True,
            'description': 'Brett Hull (8) Wrist Shot, assists: Jere Lehtinen '
                           '(3), Mike Modano (18)',
            'event': 'Goal',
            'emptyNet': False,
            'eventTypeId': 'GOAL'
        },
        'about': {
            'eventId': 6891,
            'periodTime': '14:51',
            'periodTimeRemaining': '',
            'dateTime': '1999-06-20T00:00:00Z',
            'period': 6,
            'periodType': 'OVERTIME',
            'ordinalNum': '3OT',
            'goals': {
                'away': 2,
                'home': 1
            },
            'eventIdx': 2
        },
        'team': {
            'id': 25,
            'link': '/api/v1/teams/25',
            'name': 'Dallas Stars',
            'triCode': 'DAL'
        }
    }

    NO_GOAL_PLAYS_ALL = [
        Play(period='1st',
             time='08:09',
             description='Jere Lehtinen (10) Wrist Shot, assists: Mike Modano '
                         '(17), Craig Ludwig (4)'),
        Play(period='2nd',
             time='25:19',
             description='Geoff Sanderson Interference against Derian '
                         'Hatcher'),
        Play(period='2nd',
             time='30:49',
             description='Craig Ludwig Interference against Curtis Brown'),
        Play(period='2nd',
             time='34:28',
             description='Benoit Hogue Tripping against Alexei Zhitnik'),
        Play(period='2nd',
             time='38:21',
             description='Stu Barnes (7) Slap Shot, assists: Wayne Primeau (4)'
                         ', Alexei Zhitnik (11)'),
        Play(period='2nd',
             time='39:27',
             description='Michael Peca Slashing against Richard Matvichuk'),
        Play(period='3OT',
             time='114:51',
             description='Brett Hull (8) Wrist Shot, assists: Jere Lehtinen '
                         '(3), Mike Modano (18)')
    ]

    MOCK_PLAYS = [
        Play(period='1st',
             time='00:00',
             description='Game Scheduled'),
        Play(period='1st',
             time='00:00',
             description='Period Ready'),
        Play(period='1st',
             time='00:00',
             description='Period Start'),
        Play(period='1st',
             time='00:00',
             description='Harry Potter faceoff won against Frodo Baggins'),
        Play(period='1st',
             time='00:12',
             description='Takeaway by Albus Dumbledore'),
        Play(period='1st',
             time='00:21',
             description='Albus Dumbledore - Wide of Net'),
        Play(period='1st',
             time='00:30',
             description='Ginny Weasley blocked shot from Samwise Gamgee'),
        Play(period='1st',
             time='00:31',
             description='Puck in Netting'),
        Play(period='1st',
             time='00:35',
             description='Bilbo Baggins hit Neville Longbottom'),
        Play(period='1st',
             time='01:09',
             description='Bilbo Baggins Wrist Shot saved by Oliver Wood'),
        Play(period='1st',
             time='01:27',
             description='Giveaway by Peregrin Took'),
        Play(period='1st',
             time='01:56',
             description='Goalie Stopped'),
        Play(period='1st',
             time='02:23',
             description='Luna Lovegood (2) Slap Shot, assists: Minerva '
                         'McGonagall (3), Ginny Weasley (4)'),
        Play(period='1st',
             time='07:15',
             description='Meriadoc Brandybuck Holding against Rubeus Hagrid'),
        Play(period='1st',
             time='07:15',
             description='TV timeout'),
        Play(period='1st',
             time='15:44',
             description='Offside'),
        Play(period='1st',
             time='20:00',
             description='End of 1st Period'),
        Play(period='1st',
             time='20:00',
             description='Period Official'),
        Play(period='2nd',
             time='20:23',
             description='Icing'),
        Play(period='2nd',
             time='26:09',
             description='Referee or Linesman'),
        Play(period='3rd',
             time='60:00',
             description='Game End'),
    ]

    def test01_get_schedule_known_dates(self):
        """Test that schedule can be retrieved and parsed correctly.

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

    def test06_get_last_play_no_goal(self):
        """Test that get_last_play() returns "No Goal" correctly."""
        play = nhl.get_last_play(self.NO_GOAL_GAME_ID)
        self.assertEqual(self.NO_GOAL_PLAY_ITSELF, play)

    def test07_get_plays(self):
        """Test that all events in the No Goal game parse correctly."""
        plays = nhl.get_plays(self.NO_GOAL_GAME_ID)
        self.assertEqual(7, len(plays))
        for play in plays:
            self.assertIn(nhl.get_play_tuple(play), self.NO_GOAL_PLAYS_ALL)

    def test08_get_play_tuple_no_goal(self):
        """Test that the no goal play is simplified correctly."""
        expected = Play(period='3OT',
                        time='114:51',
                        description='Brett Hull (8) Wrist Shot, assists: Jere '
                                    'Lehtinen (3), Mike Modano (18)')
        play = nhl.get_play_tuple(self.NO_GOAL_PLAY_ITSELF)
        self.assertEqual(expected, play)

    def test09_get_play_tuple_mock(self):
        """Test that mock plays are simplified correctly."""
        path = os.path.join(self.TEST_DATA, 'nhl_mock_plays.json')
        with open(path) as plays_file:
            plays = json.loads(plays_file.read())['plays']

        self.assertEqual(len(self.MOCK_PLAYS), len(plays))
        for play in plays:
            idx = play['about']['eventIdx']
            self.assertEqual(nhl.get_play_tuple(play), self.MOCK_PLAYS[idx])
