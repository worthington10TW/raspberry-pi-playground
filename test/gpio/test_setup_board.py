#!/usr/bin/env python3

import unittest
from unittest import mock

from src.gpio.setup_board import SetupBoard
from src.gpio.constants import Lights


class BoardTests(unittest.TestCase):
    @mock.patch('Mock.GPIO.setwarnings')
    def test_warningsAreDisabled(self, mocked):
        with SetupBoard((Lights.BLUE, Lights.YELLOW)):
            assert mocked.called
        args, kwargs = mocked.call_args
        self.assertEqual(False, args[0])

    @mock.patch('Mock.GPIO.cleanup')
    def test_cleanupIsCalled(self, mocked):
        with SetupBoard((Lights.BLUE, Lights.YELLOW)):
            assert not mocked.called
        assert mocked.called

    @mock.patch('Mock.GPIO.setup')
    def test_pinSetup(self, mocked):
        mocked.setup.return_value = None
        with SetupBoard((Lights.BLUE,
                         Lights.YELLOW,
                         Lights.GREEN,
                         Lights.RED)):
            calls = [mock.call(Lights.BLUE.value, 0, initial=0),
                     mock.call(Lights.YELLOW.value, 0, initial=0),
                     mock.call(Lights.GREEN.value, 0, initial=0),
                     mock.call(Lights.RED.value, 0, initial=0)]
            mocked.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
