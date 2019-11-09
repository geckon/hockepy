# vim: set fileencoding=utf-8 :

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

    # format is different for debugging
    if level == logging.DEBUG:
        formatter = logging.Formatter(
            '%(levelname)-7s: %(asctime)s : %(module)-14s: %(message)s',
            '%d-%b-%y %H:%M:%S')
    else:
        formatter = logging.Formatter('%(levelname)s: %(message)s')

    # set formatting for all handlers
    for handler in logger.handlers:
        handler.setFormatter(formatter)
