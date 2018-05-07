# vim: set fileencoding=utf-8 :

#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.game
------------

This module implements a league-agnostic Game representation.

These interfaces are implemented:
- Game named tuple
- Play named tuple
- GameStatus enum
- GameType enum
- has_started() - indicates whether the game has already started
"""

from collections import namedtuple
from enum import Enum, unique


Game = namedtuple(
    'Game',
    ['home',        # home team's name
     'away',        # away team's name
     'home_score',  # home team's score
     'away_score',  # away team's score
     'time',        # UTC time and date (datetime object)
     'type',        # GameType instance
     'status',      # GameStatus instance
     'last_play']   # last play so far - Play namedtuple or None
)


Play = namedtuple(
    'Play',
    ['period',      # displayable - e,g. '1st', '3rd', '3OT', 'SO',...
     'time',        # game time elapsed since the starts of the game
     'description']
)


def has_started(game):
    """Return true if the given game has started, False otherwise.

    Basically that means True for games that are LIVE or FINAL."""
    return game.status.value > 1


@unique
class GameStatus(Enum):
    """Game status enum."""
    SCHEDULED = 1
    LIVE = 2
    FINAL = 3

    def __str__(self):
        """Return printable representation of the status.

        That is lower case name of the status.
        """
        # pylint: disable=no-member
        # (pylint bug - see github issue #35)
        return self.name.lower()


@unique
class GameType(Enum):
    """Game type enum."""
    PRESEASON = (1, "PR")
    REGULAR = (2, "R")
    PLAYOFFS = (3, "PO")

    def __str__(self):
        """Return printable representation of the type.

        That is one or two upper case character(s) specified explicitly
        for each type.
        """
        # pylint: disable=unsubscriptable-object
        # (pylint bug - see github issue #35)
        return self.value[1]
