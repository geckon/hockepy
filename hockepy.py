#!/usr/bin/env python3
#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

import argparse
import logging
import sys

from hockepy.commands import get_commands


def init_log(debug):
    """Initialize log.

    If debug argument is true, set default level to DEBUG.
    """
    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)

    # there should be a default handler but make sure
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())

    # set formatting for all handlers
    formatter = logging.Formatter(fmt='%(levelname)s: %(module)s: %(message)s')
    for handler in logger.handlers:
        handler.setFormatter(formatter)


def run_hockepy():
    """Process arguments and run the specified sub(command)."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--debug', action='store_true',
                        help='turn debug output on')
    subparsers = parser.add_subparsers(dest='command_name')

    cmds = get_commands()
    for _, cmd_instance in cmds.items():
        cmd_instance.register_parser(subparsers)

    args = parser.parse_args(sys.argv[1:])
    if args.command_name is None:
        print("Command missing. Run `{} -h' for help.".format(sys.argv[0]))
        sys.exit(1)

    init_log(debug=args.debug)
    logging.debug('Discovered commands: %s', cmds.keys())

    command = cmds[args.command_name]
    command.run(args)
    sys.exit(0)


if __name__ == '__main__':
    run_hockepy()
