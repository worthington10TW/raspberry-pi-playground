#!/usr/bin/env python3

if __debug__:
    from Mock import GPIO
else:
    from RPi import GPIO

import logging
from time import sleep
import threading


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
        self.pulse.on()
        return self

    def __exit__(self, type, value, traceback):
        self.pulse.off()


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

    def on(self):
        self._is_pulsing = True
        logging.debug(f'Light {self.pin} pulsing')

        self.pwm = GPIO.PWM(self.pin, 100)
        dc = 0
        self.pwm.on(dc)
        # e = threading.Event()
        t = threading.Thread(name='pulse', target=self.pulse)
        t.start()
        return self

    def off(self):
        self._is_pulsing = False
        logging.debug(f'Light {self.pin} turning off')
        self.pwm.off()

    def pulse(self):
        while self.is_pulsing:
            for dc in range(0, 101, 5):
                self.pwm.ChangeDutyCycle(dc)
                sleep(0.05)
            for dc in range(95, 0, -5):
                self.pwm.ChangeDutyCycle(dc)
                sleep(0.05)

    @property
    def is_pulsing(self):
        return self._is_pulsing
