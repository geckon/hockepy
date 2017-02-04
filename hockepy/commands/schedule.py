#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockeypy.commands.schedule
------------------------------

This module defines class for schedule command.

The purpose of this command is to retrieve and print information about
games scheduled for the given date (default is today).
"""

import datetime

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
        parser = subparsers.add_parser('schedule')
        parser.add_argument('date', help='date to get schedule for',
                            default=None, nargs='?')
        return parser

    def run(self, args):
        """Run the command with the given arguments."""
        if args.date is None:
            date = datetime.date.today().strftime(self.DATE_FMT)
        else:
            date = args.date

        games = nhl.get_schedule(date)
        if not games:
            print('No games for today.')
        else:
            max_name_len = max([len(game.away) for game in games])
            for game in games:
                print('{away:>{width}} @ {home}'.format(
                    away=game.away, home=game.home, width=max_name_len))
