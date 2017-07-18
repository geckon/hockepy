# -*- coding: utf-8 -*-

#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.log
------------

This module contains logging-related code:
- init_log() function initializes the logger.
- HockepyFormatter class specifies format of log messages.
"""

import logging


def init_log(level=logging.WARNING):
    """Initialize log.

    WARNING is the default log level but it can be overridden.
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    # there should be a default handler but make sure
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())

    # set formatting for all handlers
    formatter = HockepyFormatter()
    for handler in logger.handlers:
        handler.setFormatter(formatter)


class HockepyFormatter(logging.Formatter):
    """Default formatter for hockepy.

    Allows setting different format for each log level which is
    accomplished by keeping multiple formatters internally and calling
    the right one for each log record.
    """

    FORMATTERS = {
        logging.INFO: logging.Formatter(
            fmt='%(levelname)s: %(message)s'),
        'DEFAULT': logging.Formatter(
            fmt='%(levelname)-7s: %(module)-14s: %(message)s')
        }

    def format(self, record):
        """Format the given record according to its log level."""
        formatter = self.FORMATTERS.get(
            record.levelno, self.FORMATTERS['DEFAULT'])
        return formatter.format(record)
