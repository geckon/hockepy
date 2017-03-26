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
    actual command (a class derived from BaseCommand) only has to define
    its '_COMMAND' class variable and it will be returned as their
    'command' property.
    """

    @property
    def command(cls):
        """Return command name as defined by the class.

        This only implements a "pure" class property and won't work if
        called on instances - for that classes need to add their
        property (see BaseCommand). Such property is inheritable though
        and will work for derived classes correctly as long as they set
        their own '_COMMAND' class variable.
        The reason is that meta classes are not included into the lookup
        chain when accessing attributes. For more information read:
        https://docs.python.org/3/howto/descriptor.html
        (especially the 'Definition and Introduction' section)
        """
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

    @property
    def command(self):
        """Return the command name as expected on the command line.

        Thanks to BaseCommandMeta meta class, the derived classes only
        need to specify their '_COMMAND' class variable and it will
        work as intended.
        It might seem redundant to implement this when we have the class
        property added by BaseCommandMeta but without this it wouldn't
        work for instances - see the docstring explaining the property
        implemented by the meta class.
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
