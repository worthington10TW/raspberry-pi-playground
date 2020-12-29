#!/usr/bin/env python3

import unittest
from unittest import mock

from src.gpio.board import Board
from src.gpio.constants import Lights


class BoardTests(unittest.TestCase):
    @mock.patch('Mock.GPIO.setwarnings')
    def test_warningsAreDisabled(self, mocked):
        with Board():
            assert mocked.called
        args, kwargs = mocked.call_args
        self.assertEqual(False, args[0])

    @mock.patch('Mock.GPIO.cleanup')
    def test_cleanupIsCalled(self, mocked):
        with Board():
            assert not mocked.called
        assert mocked.called

    @mock.patch('Mock.GPIO.setup')
    def test_pinSetup(self, mocked):
        mocked.setup.return_value = None
        with Board():
            calls = [mock.call(Lights.GREEN.value, 0, initial=0),
                     mock.call(Lights.YELLOW.value, 0, initial=0),
                     mock.call(Lights.RED.value, 0, initial=0),
                     mock.call(Lights.BLUE.value, 0, initial=0)]
            mocked.assert_has_calls(calls)

    @mock.patch('Mock.GPIO.output')
    def test_turn_on(self, mocked):
        with Board() as board:
            board.on(Lights.BLUE)
            mocked.assert_called_with(Lights.BLUE.value, 1)

    @mock.patch('Mock.GPIO.output')
    def test_turn_off(self, mocked):
        with Board() as board:
            board.off(Lights.BLUE)
            mocked.assert_called_with(Lights.BLUE.value, 0)

    @mock.patch('Mock.GPIO.PWM')
    def test_pulse(self, mocked):
        mocked.return_value.ChangeDutyCycle = mock.MagicMock()
        mocked.return_value.stop = mock.MagicMock()
        with Board() as board:
            board.pulse(Lights.BLUE)
            mocked.assert_called_with(Lights.BLUE.value, 100)
            board.off(Lights.BLUE)
            assert mocked.return_value.stop.called
            mocked.return_value.ChangeDutyCycle.called


if __name__ == '__main__':
    unittest.main()
