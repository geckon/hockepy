# vim: set fileencoding=utf-8 :

#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.commands
-----------------

This module provides definition of hockepy (sub)commands as well as
a function to retrieve all available (sub)commands.
"""

from hockepy.commands.base_command import BaseCommand
from hockepy.commands.schedule import Schedule
from hockepy.commands.today import Today


def get_commands():
    """Return all available commands.

    More specifically, return a dictionary where keys are commands'
    names and values are the classes themselves. Cache the dictionary
    for repeated use.
    """
    return BaseCommand.get_commands()
