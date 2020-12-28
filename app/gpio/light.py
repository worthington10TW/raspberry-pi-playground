#!/usr/bin/env python3

if __debug__:
    from Mock import GPIO
else:
    from RPi import GPIO

import logging
import asyncio
from time import sleep


class LightWrapper:
    def __init__(self, pin):
        self.light = Light(pin)

    def __enter__(self):
        self.light.on()
        return self

    def __exit__(self, type, value, traceback):
        self.light.off()


class PulseWrapper:
    def __init__(self, pin):
        self.pulse = Pulse(pin)

    def __enter__(self):
        self.pulse.start()
        return self

    def __exit__(self, type, value, traceback):
        self.pulse.stop()


class Light:
    def __init__(self, pin):
        self.pin = pin

    def on(self):
        logging.debug(f'Light {self.pin} turning on...')
        GPIO.output(self.pin, GPIO.HIGH)
        logging.debug(f'Light {self.pin} on')

    def off(self):
        logging.debug(f'Light {self.pin} turning off...')
        GPIO.output(self.pin, GPIO.LOW)
        logging.debug(f'Light {self.pin} off')


class Pulse:
    def __init__(self, pin):
        self.pin = pin
        self._is_pulsing = False
        self.pwm = GPIO.PWM(self.pin, 100)
        dc = 0
        self.pwm.start(dc)

    def start(self):
        self._is_pulsing = True
        logging.debug(f'Light {self.pin} pulsing')

        while self._is_pulsing
            for dc in range(0, 101, 5):
                self.pwm.ChangeDutyCycle(dc)
                sleep(0.05)
                print(dc)
            for dc in range(95, 0, -5):
                self.pwm.ChangeDutyCycle(dc)
                sleep(0.05)
                print(dc)

        asyncio.ensure_future(self.__pulse())
        return self

    def stop(self):
        self._is_pulsing = False
        logging.debug(f'Light {self.pin} turning off')
        self.pwm.stop()

    async def __pulse(self):
        while self.is_pulsing:
            for dc in range(0, 101, 5):
                self.pwm.ChangeDutyCycle(dc)
                await asyncio.sleep(0.01)
            for dc in range(95, 0, -5):
                self.pwm.ChangeDutyCycle(dc)
                await asyncio.sleep(0.01)

    @property
    def is_pulsing(self):
        return self._is_pulsing
