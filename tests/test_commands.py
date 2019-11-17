# vim: set fileencoding=utf-8 :

#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.commands module tests
------------------------
"""

import time
import unittest

from hockepy import commands


class TestCommands(unittest.TestCase):
    """Tests for hockepy.commands module.
    """

    def test01_command_registration(self):
        """Test that commands are properly registered."""

        class DummyCommand(commands.BaseCommand):
            _COMMAND = 'dummy_command'

        self.assertIn(DummyCommand._COMMAND,
                      commands.BaseCommand.get_commands())

    def test02_abstract_command_registration(self):
        """Test that abstract commands are not registered."""

        class AbstractDummyCommand(commands.BaseCommand, is_abstract=True):
            _COMMAND = 'abstract_dummy_command'

        self.assertNotIn(AbstractDummyCommand._COMMAND,
                         commands.BaseCommand.get_commands())
