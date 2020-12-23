#!/usr/bin/python3
if __debug__:
    import Mock.GPIO
    GPIO = Mock.GPIO
else:
    from RPi import GPIO

import time
import asyncio
from logger import setup_logger


async def prettyShow(logger, pins):
    while (True):
        for pin in pins:
            GPIO.output(pin, not GPIO.input(pin))
            await asyncio.sleep(0.1)

async def pulse(logger, pin):
    try:
        pwm = GPIO.PWM(pin, 100)
        dc = 0
        pwm.start(dc)
        while (True):
            for dc in range(0, 101, 5):
                pwm.ChangeDutyCycle(dc)
                await asyncio.sleep(0.05)
            for dc in range(95, 0, -5):
                pwm.ChangeDutyCycle(dc)
                await asyncio.sleep(0.05)
    finally:
        pwm.stop()

async def main():
    try:
        logger = setup_logger('blink.py')

        logger.info('Starting blink program')
        GREEN = 17
        YELLOW = 22
        RED = 27
        BLUE = 18

        logger.info('Setting up GPIO')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(GREEN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(RED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(YELLOW, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(BLUE, GPIO.OUT, initial=GPIO.LOW)

        asyncio.ensure_future(pulse(logger, BLUE))
        # asyncio.ensure_future(pulse(logger, RED))
        # asyncio.ensure_future(pulse(logger, YELLOW))
        # await asyncio.ensure_future(pulse(logger, GREEN))
        await prettyShow(logger, (GREEN, RED, YELLOW))
    except KeyboardInterrupt:
        pass
    finally:
        logger.info('Finishing up')
        GPIO.cleanup()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
