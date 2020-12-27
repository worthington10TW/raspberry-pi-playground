#!/usr/bin/env python3

import unittest
from unittest import mock

from app import setup_board


class SetupTests(unittest.TestCase):
    @mock.patch('Mock.GPIO.setwarnings')
    def test_warningsAreDisabled(self, mocked):
        with setup_board.SetupBoard((1, 2, 3, 4)):
            assert mocked.called
        args, kwargs = mocked.call_args
        self.assertEqual(False, args[0])

    @mock.patch('Mock.GPIO.cleanup')
    def test_cleanupIsCalled(self, mocked):
        with setup_board.SetupBoard((1, 2, 3, 4)):
            assert not mocked.called
        assert mocked.called

    @mock.patch('Mock.GPIO.setup')
    def test_pinSetup(self, mocked):
        mocked.setup.return_value = None
        with setup_board.SetupBoard((1, 2, 3, 4)):
            calls = [mock.call(1, 0, initial=0),
                     mock.call(2, 0, initial=0),
                     mock.call(3, 0, initial=0),
                     mock.call(4, 0, initial=0)]
            mocked.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
