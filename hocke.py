#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :

#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.py
-----------

hockepy.py CLI utility implementation.

Run with -h for help.
"""

import argparse
import logging
import sys

from hockepy.commands import get_commands
from hockepy.config import init_config
from hockepy.log import init_log
from hockepy.utils import exit_error


def process_args(parser):
    """Parse, process and return arguments.

    Also initialize logger. Exit, if there is an error (e.g. no command
    provided).
    """
    args = parser.parse_args(sys.argv[1:])

    # initialize log
    if args.debug:
        loglevel = logging.DEBUG
    elif args.verbose:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING
    init_log(level=loglevel)
    logging.debug('Logging level set to %s', loglevel)

    # check that we have a command
    if args.command_name is None:
        exit_error(f"Command missing. Run `{sys.argv[0]} -h' for help.")

    return args


def run_hockepy():
    """Process arguments and run the specified sub(command)."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--debug', action='store_true', dest='debug',
                        help='turn debug output on')
    parser.add_argument('-v', '--verbose', action='store_true',
                        dest='verbose', help='turn verbose output on')
    subparsers = parser.add_subparsers(dest='command_name')

    cmds = get_commands()
    for cmd_instance in cmds.values():
        cmd_instance.register_parser(subparsers)

    args = process_args(parser)

    init_config()

    logging.debug('Discovered commands: %s', cmds.keys())
    # Initialize and run the requested command.
    command = cmds[args.command_name](args)
    command.run()
    sys.exit(0)


if __name__ == '__main__':
    run_hockepy()
