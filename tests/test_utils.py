# vim: set fileencoding=utf-8 :

#  ____  ____    ____      ______  ___  ____   _________  ______    ____  ____
# |_   ||   _| .'    `.  .' ___  ||_  ||_  _| |_   ___  ||_   __ \ |_  _||_  _|
#   | |__| |  /  .--.  \/ .'   \_|  | |_/ /     | |_  \_|  | |__) |  \ \  / /
#   |  __  |  | |    | || |         |  __'.     |  _|  _   |  ___/    \ \/ /
#  _| |  | |_ \  `--'  /\ `.___.'\ _| |  \ \_  _| |___/ | _| |_       _|  |_
# |____||____| `.____.'  `._____.'|____||____||_________||_____|     |______|
#

"""
hockepy.utils module tests
------------------------
"""

import time
import unittest

from hockepy import utils


class TestUtils(unittest.TestCase):
    """Tests for hockepy.utils module.
    """

    def test01_bold(self):
        """Test that bold text works as expected."""

        self.assertEqual('\033[1mHello world!\033[0m',
                         utils.bold_text('Hello world!'))
        self.assertEqual(8, utils.bold_escape_seq_width())

    def test02_exit_error(self):
        """Test that exit_error() actually exits with exit code 1."""
        with self.assertRaises(SystemExit) as sysexit:
            utils.exit_error()
            unittest.main(exit=False)
        self.assertEqual(1, sysexit.exception.code)

    def test03_local_timezone(self):
        """Test that local timezone is determined correctly."""
        self.assertEqual(time.localtime().tm_zone, str(utils.local_timezone()))
