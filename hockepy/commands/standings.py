# vim: set fileencoding=utf-8 :

#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.commands.standings
-----------------------

This module defines class for standings command.

The purpose of this command is to retrieve and print the current
standings as a table.
"""

import logging

from hockepy import nhl
from hockepy.commands import BaseCommand

from prettytable import PrettyTable

class Standings(BaseCommand):
    """Standings command.

    Accepts the following arguments:
    """

    _COMMAND = 'standings'

    @property
    def description(self):
        """Return the command's short description for user."""
        return 'Print the current standings.'

    @classmethod
    def register_parser(cls, subparsers):
        """Register and return the sub-command's parser."""
        pass

    def run(self):
        """Run the command with the given arguments."""
        logging.debug('Running the %r command.', self.command)
        standings = nhl.get_standings()
