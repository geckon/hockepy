#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.commands.base_command
------------------------------

This module contains abstract class BaseCommand that specifies interface
for all hockepy (sub)commands. BaseCommandMeta class is defined and used
for convenience - it adds 'command' class property.
"""

import abc


class BaseCommandMeta(abc.ABCMeta):
    """Meta class for BaseCommand.

    It works just as abc.ABCMeta but it adds one more thing - a class
    property 'command' that each command should have. This way each
    command (a class derived from BaseCommand) only has to define its
    '_COMMAND' and it will work as their 'command' property.
    """

    @property
    def command(cls):
        """Return command name as defined by the class."""
        return cls._COMMAND


class BaseCommand(metaclass=BaseCommandMeta):
    """Abstract class definining the interface each hockepy (sub)command
    should implement.
    """

    # This needs to be overwritten by every subclass.
    _COMMAND = None

    def __init__(self, args=None):
        """Initialize the command."""
        self.args = args

    def command(self):
        """Return the command name as expected on the command line.

        Thanks to BaseCommandMeta meta class, the derived classes only
        need to specify their '_COMMAND' member variable and it will
        work as intended.
        """
        return type(self).command

    @abc.abstractproperty
    def description(self):
        """Return the command's short description for user."""

    @abc.abstractmethod
    def register_parser(self, subparsers):
        """Register and return the sub-command's parser.

        It needs to be implemented as a @classmethod."""

    @abc.abstractmethod
    def run(self):
        """Run the command."""
