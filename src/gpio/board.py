#!/usr/bin/env python3

if __debug__:
    from Mock import GPIO
else:
    from RPi import GPIO

import logging
import asyncio

from .constants import Lights


class Board(object):
    def __enter__(self):
        logging.info('Setting up GPIO')
        self.GPIO = GPIO

        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.pwm = {}
        self.tasks = {}
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
        if light in self.tasks:
            self.tasks[light].cancel()
            del self.tasks[light]

        logging.debug(f'Light {light} turning off...')
        self.GPIO.output(light.value, self.GPIO.LOW)
        logging.debug(f'Light {light} off')

    async def pulse(self, light):
        if light in self.tasks:
            logging.debug(f'Light {light} is already pulsing.')
            return

        dc = 0
        pwm = self.pwm[light]
        pwm.start(dc)

        self.tasks[light] = asyncio.ensure_future(pulse(pwm))
        logging.debug(f'Light {light} pulsing...')
        await asyncio.sleep(0.001)

    def __exit__(self, type, value, traceback):
        logging.info('Cleaning up GPIO')
        self.GPIO.cleanup()


async def pulse(pwm):
    while True:
        for dc in range(0, 101, 5):
            pwm.ChangeDutyCycle(dc)
            await asyncio.sleep(0.05)
        for dc in range(95, 0, -5):
            pwm.ChangeDutyCycle(dc)
            await asyncio.sleep(0.05)
