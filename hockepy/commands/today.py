#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockeypy.commands.today
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

    @property
    def command(self):
        """Return the command name as expected on the command line."""
        return 'today'

    @property
    def description(self):
        """Return the command's short description for user."""
        return 'Print schedule for today.'

    def register_parser(self, subparsers):
        """Register and return the sub-command's parser."""
        parser = subparsers.add_parser(self.command)
        return parser

    def run(self, args):
        """Run the command with the given arguments."""
        logging.debug('Running the %r command.', self.command)
        args.date = None
        Schedule().run(args)
