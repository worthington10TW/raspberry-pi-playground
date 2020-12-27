#!/usr/bin/env python3

if __debug__:
    from Mock import GPIO
else:
    from RPi import GPIO

import logging
import asyncio


class Light:
    def __init__(self, pin):
        self.pin = pin

    def on(self):
        logging.debug(f'Light {self.pin} turning on...TESTAgain')
        GPIO.output(self.pin, GPIO.HIGH)
        logging.debug(f'Light {self.pin} on')

    def off(self):
        logging.debug(f'Light {self.pin} turning off...')
        GPIO.output(self.pin, GPIO.LOW)
        logging.debug(f'Light {self.pin} off')

    async def __pulse(self):
        try:
            pwm = GPIO.PWM(self.pin, 100)
            dc = 0
            pwm.start(dc)
            while self.pulse:
                for dc in range(0, 101, 5):
                    pwm.ChangeDutyCycle(dc)
                    await asyncio.sleep(0.05)
                for dc in range(95, 0, -5):
                    pwm.ChangeDutyCycle(dc)
                    await asyncio.sleep(0.05)
        finally:
            logging('Pulse stopped')
            pwm.stop()
