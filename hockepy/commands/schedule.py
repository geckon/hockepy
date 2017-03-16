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


class Schedule(BaseCommand):
    """Schedule command.

    Accepts the following arguments:
    - date (positional)
    """

    DATE_FMT = '%Y-%m-%d'

    @property
    def command(self):
        """Return the command name as expected on the command line."""
        return 'schedule'

    @property
    def description(self):
        """Return the command's short description for user."""
        return 'Print schedule for the requested date.'

    def register_parser(self, subparsers):
        """Register and return the sub-command's parser."""
        parser = subparsers.add_parser(self.command)
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
        time = '{h:02d}:{m:02d} UTC'.format(
            h=game.time.tm_hour, m=game.time.tm_min)
        print(teams + time)

    def run(self, args):
        """Run the command with the given arguments."""
        logging.debug('Running the %r command.', self.command)
        if args.first_date is None:
            args.first_date = datetime.date.today().strftime(self.DATE_FMT)
            logging.debug('Date empty -> using today (%s).', args.first_date)
        if args.last_date is None:
            args.last_date = args.first_date
        self.args = args

        schedule = nhl.get_schedule(args.first_date, args.last_date)
        if schedule is None:
            print('No games at all.')
            return
        for date, games in schedule.items():
            print('Schedule for {}'.format(date))
            if not games:
                print('  No games for {}.'.format(date))
            else:
                # + 1 is an additional padding
                team_width = max([len(game.home) for game in games]) + 1
                for game in games:
                    self.print_game(game, team_width)
            print('')
