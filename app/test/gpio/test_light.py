#!/usr/bin/env python3

import unittest
from unittest import mock
from app.gpio.light import Light, PulseWrapper


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
        with PulseWrapper(1) as light:
            self.assertEqual(True, light.is_pulsing)
            mocked.return_value.stop.assert_not_called()

        mocked.assert_called_once_with(1, 100)
        self.assertEqual(False, light.is_pulsing)
        assert mocked.return_value.stop.called


if __name__ == '__main__':
    unittest.main()
