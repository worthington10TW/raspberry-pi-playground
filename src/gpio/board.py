#!/usr/bin/env python3

if __debug__:
    from Mock import GPIO
else:
    from RPi import GPIO

import logging
import threading
import time
from .constants import Lights


class Board(object):
    def __enter__(self):
        logging.info('Setting up GPIO')
        self.GPIO = GPIO

        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.pwm = {}
        for light in Lights:
            self.GPIO.setup(
                light.value,
                self.GPIO.OUT,
                initial=self.GPIO.LOW)
            self.pwm[light] = self.GPIO.PWM(
                light.value,
                100)

        return self

    def on(self, light):
        logging.debug(f'Light {light} turning on...')
        self.GPIO.output(light.value, self.GPIO.HIGH)
        logging.debug(f'Light {light} on')

    def off(self, light):
        if light in self.pwm:
            self.pwm[light].stop()

        logging.debug(f'Light {light} turning off...')
        self.GPIO.output(light.value, self.GPIO.LOW)
        logging.debug(f'Light {light} off')

    def pulse(self, light):
        dc = 0
        self.pwm[light].start(dc)

        logging.debug(f'Light {light} pulsing...')
        pwm = self.pwm[light]
        task = threading.Thread(name='pulse', target=pulse, args=(pwm,))
        task.start()

    def __exit__(self, type, value, traceback):
        logging.info('Cleaning up GPIO')
        self.GPIO.cleanup()


def pulse(pwm):
    try:
        while True:
            for dc in range(0, 101, 5):
                pwm.ChangeDutyCycle(dc)
                time.sleep(0.05)
            for dc in range(95, 0, -5):
                pwm.ChangeDutyCycle(dc)
                time.sleep(0.05)
    except KeyboardInterrupt:
        pass
