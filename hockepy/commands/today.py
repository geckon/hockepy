#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.commands.today
-----------------------

This module defines class for today command.

This command is very similar to 'schedule' command and it's purpose is
to retrieve and print information about games scheduled for today.
"""

import logging

from hockepy.commands import BaseCommand, Schedule


class Today(BaseCommand):
    """Today command.

    Accepts the following arguments:
    """

    _COMMAND = 'today'

    @property
    def description(self):
        """Return the command's short description for user."""
        return 'Print schedule for today.'

    @classmethod
    def register_parser(cls, subparsers):
        """Register and return the sub-command's parser."""
        parser = subparsers.add_parser(cls.command)
        parser.add_argument('--home-first', dest='home_first',
                            action='store_true',
                            help='print the home team first')
        return parser

    def run(self):
        """Run the command with the given arguments."""
        logging.debug('Running the %r command.', self.command)
        self.args.first_date = self.args.last_date = None
        Schedule(self.args).run()
