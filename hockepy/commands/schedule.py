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
from hockepy.commands import BaseCommand
from hockepy.utils import datetime_to_local


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
        return parser

    def print_game(self, game, team_width):
        """Print the given game.

        Respect 'home_first' argument and use the appropriate delimiter.
        Also print each team name so it's padded to at least
        'team_width' characters. Print each game on one line.
        """
        if self.args.home_first:
            teams_fmt = '{home:>{width}} : {away:<{width}}'
        else:
            teams_fmt = '{away:>{width}} @ {home:<{width}}'
        teams = teams_fmt.format(
            away=game.away, home=game.home, width=team_width)
        gametime = datetime_to_local(game.time)
        time = '{h:02d}:{m:02d} {tz}'.format(
            h=gametime.hour, m=gametime.minute, tz=gametime.tzname())
        print(teams + time)

    def run(self):
        """Run the command."""
        logging.debug('Running the %r command.', self.command)
        if self.args.first_date is None:
            self.args.first_date = datetime.date.today().strftime(
                self.DATE_FMT)
            logging.debug('Date empty -> using today (%s).',
                          self.args.first_date)
        if self.args.last_date is None:
            self.args.last_date = self.args.first_date

        schedule = nhl.get_schedule(self.args.first_date, self.args.last_date)
        if schedule is None:
            print('No games at all.')
            return
        for date, games in schedule.items():
            print('Schedule for {}'.format(date))
            if not games:
                print('  No games for {}.'.format(date))
            else:
                home_width = max([len(game.home) for game in games])
                away_width = max([len(game.away) for game in games])
                # + 1 is an additional padding
                team_width = max(home_width, away_width) + 1
                for game in games:
                    self.print_game(game, team_width)
            print('')
