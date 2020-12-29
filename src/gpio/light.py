#!/usr/bin/env python3

if __debug__:
    from Mock import GPIO
else:
    from RPi import GPIO

import logging
from time import sleep
import threading


class LightWrapper:
    def __init__(self, light):
        self.light = Light(light)

    def __enter__(self):
        self.light.on()
        return self

    def __exit__(self, type, value, traceback):
        self.light.off()


class PulseWrapper:
    def __init__(self, light):
        self.pulse = Pulse(light)

    def __enter__(self):
        self.pulse.on()
        return self

    def __exit__(self, type, value, traceback):
        self.pulse.off()


class Light:
    def __init__(self, light):
        self.light = light

    def on(self):
        logging.debug(f'Light {self.light} turning on...')
        GPIO.output(self.light.value, GPIO.HIGH)
        logging.debug(f'Light {self.light} on')

    def off(self):
        logging.debug(f'Light {self.light} turning off...')
        GPIO.output(self.light.value, GPIO.LOW)
        logging.debug(f'Light {self.light} off')


class Pulse:
    def __init__(self, light):
        self.light = light
        self._is_pulsing = False
        self.pwm = GPIO.PWM(self.light.value, 100)

    def on(self):
        self._is_pulsing = True
        dc = 0
        self.pwm.start(dc)
        logging.debug(f'Light {self.light} pulsing')
        self.task = threading.Thread(name='pulse', target=self.pulse)
        self.task.start()
        return self

    def off(self):
        self._is_pulsing = False
        logging.debug(f'Light {self.light} turning off')
        self.pwm.stop()

    @property
    def is_pulsing(self):
        return self._is_pulsing

    def pulse(self):
        while self.is_pulsing:
            for dc in range(0, 101, 5):
                self.pwm.ChangeDutyCycle(dc)
                sleep(0.05)
            for dc in range(95, 0, -5):
                self.pwm.ChangeDutyCycle(dc)
                sleep(0.05)