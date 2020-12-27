#!/usr/bin/env python3

import unittest
from unittest import mock
from app.light import Light


class SetupTests(unittest.TestCase):
    @mock.patch('Mock.GPIO.output')
    def test_turn_on(self, mocked):
        light = Light(1)
        light.on()
        mocked.assert_called_with(1, 1)

    @mock.patch('Mock.GPIO.output')
    def test_turn_off(self, mocked):
        light = Light(1)
        light.off()
        mocked.assert_called_with(1, 0)


if __name__ == '__main__':
    unittest.main()
