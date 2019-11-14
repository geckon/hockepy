# vim: set fileencoding=utf-8 :

#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.commands.schedule
------------------------------

This module defines class for schedule command.

The purpose of this command is to retrieve and print information about
games scheduled for the given date (default is today).
"""

import datetime
import logging

from hockepy import nhl
from hockepy.config import CONF
from hockepy.commands import BaseCommand
from hockepy.game import has_started, GameStatus
from hockepy.utils import (bold_text, bold_escape_seq_width, exit_error,
                           local_timezone)


class Schedule(BaseCommand):
    """Schedule command.

    Accepts the following arguments:
    - date (positional)
    """

    _COMMAND = 'schedule'
    DATE_FMT = '%Y-%m-%d'

    @property
    def description(self):
        """Return the command's short description for user."""
        return 'Print schedule for the requested date.'

    @classmethod
    def register_parser(cls, subparsers):
        """Register and return the sub-command's parser."""
        parser = subparsers.add_parser(cls.command)
        parser.add_argument('first_date', default=None, nargs='?',
                            help='first date to get schedule for')
        parser.add_argument('last_date', default=None, nargs='?',
                            help='last date to get schedule for')
        parser.add_argument('--home-first', dest='home_first',
                            action='store_true',
                            help='print the home team first')
        parser.add_argument('--utc', dest='utc', action='store_true',
                            help='print times in UTC instead of local time')
        return parser

    @staticmethod
    def get_time_txt(game, timezone=None):
        """Compose game's time as a text to be printed."""
        if timezone:
            gametime = game.time.astimezone(timezone)
        else:
            gametime = game.time

        return f'{gametime.hour:02d}:{gametime.minute:02d} {gametime.tzname()}'

    @staticmethod
    def get_score_txt(game, score_fmt):
        """"Compose game's score as a text to be printed."""
        if has_started(game):
            score = score_fmt.format(away=game.away_score,
                                     home=game.home_score)
            if game.last_play.period == 'SO' or game.last_play.period == 'OT':
                return score + ' ' + game.last_play.period
            return score + '   '

        # the game has not started yet -> don't display score
        return '      '

    @staticmethod
    def get_last_play_txt(game):
        """Compose game's last play as a text to be printed."""
        if game.status == GameStatus.LIVE and game.last_play:
            return f'- {game.last_play.description} ({game.last_play.time})'

        # the game has finished or has not started yet
        # -> the last play is not relevant
        return ''

    def print_game(self, game, team_width, timezone=None):
        """Print the given game.

        Respect 'home_first' argument and use the appropriate delimiter.
        Also print each team name so it's padded to at least
        'team_width' characters.
        If tz is provided, print time in this time zone. Otherwise use
        the game time's time zone.
        Print each game on one line.
        """
        logging.debug('Printing game %s', game)

        gametype = f'{game.type:2}'

        home_width = away_width = team_width

        # highight teams
        width_compensation = bold_escape_seq_width()
        if game.home in CONF['highlight_teams']:
            game = game._replace(home=bold_text(game.home))
            home_width = home_width + width_compensation
        if game.away in CONF['highlight_teams']:
            game = game._replace(away=bold_text(game.away))
            away_width = away_width + width_compensation

        if self.args.home_first:
            teams_fmt = '{home:>{home_w}} : {away:<{away_w}}'
            score_fmt = '{home}:{away}'
        else:
            teams_fmt = '{away:>{away_w}} @ {home:<{home_w}}'
            score_fmt = '{away}:{home}'
        teams = teams_fmt.format(away=game.away, home=game.home,
                                 away_w=away_width, home_w=home_width)

        time = Schedule.get_time_txt(game, timezone)
        score = Schedule.get_score_txt(game, score_fmt)
        last_play = Schedule.get_last_play_txt(game)
        status = f'({game.status})'

        print(' '.join((gametype, teams, time, score, status, last_play)))

    def print_schedule(self, schedule, local_tz):
        """Print the schedule."""
        if schedule is None:
            print('No games at all.')
            return
        for date, games in schedule.items():
            print(f'Schedule for {date}')
            if not games:
                print(f'  No games for {date}.')
            else:
                home_width = max([len(game.home) for game in games])
                away_width = max([len(game.away) for game in games])
                # + 1 is an additional padding
                team_width = max(home_width, away_width) + 1
                for game in games:
                    self.print_game(game, team_width, local_tz)
            print('')

    def run(self):
        """Run the command."""
        logging.debug('Running the %r command.', self.command)

        # Determine the date(s) the schedule is wanted for.
        if self.args.first_date is None:
            self.args.first_date = datetime.date.today().strftime(
                self.DATE_FMT)
            logging.debug('Date empty -> using today (%s).',
                          self.args.first_date)
        if self.args.last_date is None:
            self.args.last_date = self.args.first_date
        try:
            datetime.datetime.strptime(self.args.first_date, self.DATE_FMT)
            datetime.datetime.strptime(self.args.last_date, self.DATE_FMT)
        except ValueError:
            exit_error(f'Dates must be in {self.DATE_FMT!r} format.')

        # Should local time be considered or UTC?
        if self.args.utc:
            local_tz = None
        else:
            local_tz = local_timezone()

        # Get the schedule and print it.
        schedule = nhl.get_schedule(self.args.first_date, self.args.last_date)
        self.print_schedule(schedule, local_tz)
