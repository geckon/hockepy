#!/usr/bin/env python3
#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

import argparse
import sys

from hockepy.commands import get_commands

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print("Command missing. Run `{} -h' for help.".format(sys.argv[0]))
        sys.exit(1)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command_name')

    cmds = get_commands()
    for cmd, cmd_instance in cmds.items():
        cmd_instance.register_parser(subparsers)

    args = parser.parse_args(sys.argv[1:])
    command = cmds[args.command_name]
    command.run(args)
    sys.exit(0)
