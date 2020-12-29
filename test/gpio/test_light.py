#!/usr/bin/env python3

import unittest
from unittest import mock
from src.gpio.light import Light, Pulse


class LightTests(unittest.TestCase):
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

    @mock.patch('Mock.GPIO.PWM')
    def test_pulse_pwm_setup(self, mocked):
        mocked.return_value.stop = mock.MagicMock()
        pulse = Pulse(1)
        pulse.on()
        self.assertEqual(True, pulse.is_pulsing)
        mocked.assert_called_once_with(1, 100)
        pulse.off()
        self.assertEqual(False, pulse.is_pulsing)
        assert mocked.return_value.stop.called


if __name__ == '__main__':
    unittest.main()
