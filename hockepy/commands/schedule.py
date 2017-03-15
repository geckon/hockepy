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

    def run(self, args):
        """Run the command with the given arguments."""
        logging.debug('Running the %r command.', self.command)
        if args.first_date is None:
            args.first_date = datetime.date.today().strftime(self.DATE_FMT)
            logging.debug('Date empty -> using today (%s).', args.first_date)
        if args.last_date is None:
            args.last_date = args.first_date

        schedule = nhl.get_schedule(args.first_date, args.last_date)
        if schedule is None:
            print('No games at all.')
            return
        for date, games in schedule.items():
            print('Schedule for {}'.format(date))
            if not games:
                print('  No games for {}.'.format(date))
            else:
                if args.home_first:
                    game_fmt = '  {home:>{width}} : {away}'
                    max_first_len = max([len(game.home) for game in games])
                else:
                    game_fmt = '  {away:>{width}} @ {home}'
                    max_first_len = max([len(game.away) for game in games])
                for game in games:
                    print(game_fmt.format(
                        away=game.away, home=game.home, width=max_first_len))
            print('')
