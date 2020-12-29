#!/usr/bin/env python3

if __debug__:
    from Mock import GPIO
else:
    from RPi import GPIO

import logging


class SetupBoard(object):
    def __init__(self, lights):
        self.lights = lights

    def __enter__(self):
        logging.info('Setting up GPIO')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        [GPIO.setup(light.value, GPIO.OUT, initial=GPIO.LOW)
            for light in self.lights]

    def on(self, light):
        logging.info(f'Turning light on {light}')

    def off(self, light):
        logging.info(f'Turning light off {light}')

    def __exit__(self, type, value, traceback):
        logging.info('Cleaning up GPIO')
        GPIO.cleanup()
