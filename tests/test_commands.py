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

import unittest

from hockepy import commands


class TestCommands(unittest.TestCase):
    """Tests for hockepy.commands module.
    """

    def test01_command_registration(self):
        """Test that commands are properly registered."""

        # pylint: disable=W0612
        # (ignore unused-variable DummyCommand)
        class DummyCommand(commands.BaseCommand):
            """Dummy command.
            """

            _COMMAND = 'dummy_command'

            @property
            def description(self):
                pass

            @classmethod
            def register_parser(cls, subparsers):
                pass

            def run(self):
                pass

        self.assertIn('dummy_command',
                      commands.BaseCommand.get_commands())

    def test02_abstract_command_registration(self):
        """Test that abstract commands are not registered."""

        # pylint: disable=W0612
        # (ignore unused-variable AbstractDummyCommand)
        class AbstractDummyCommand(commands.BaseCommand, is_abstract=True):
            """Dummy abstract command.
            """

            _COMMAND = 'abstract_dummy_command'

            @property
            def description(self):
                pass

            @classmethod
            def register_parser(cls, subparsers):
                pass

            def run(self):
                pass

        self.assertNotIn('abstract_dummy_command',
                         commands.BaseCommand.get_commands())
