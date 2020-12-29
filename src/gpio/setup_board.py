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
        logging.debug(f'Light {light} turning on...')
        GPIO.output(light.value, GPIO.HIGH)
        logging.debug(f'Light {light} on')

    def off(self, light):
        logging.debug(f'Light {light} turning off...')
        GPIO.output(light.value, GPIO.LOW)
        logging.debug(f'Light {light} off')

    def __exit__(self, type, value, traceback):
        logging.info('Cleaning up GPIO')
        GPIO.cleanup()
