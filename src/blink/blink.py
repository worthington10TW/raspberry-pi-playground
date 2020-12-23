#!/usr/bin/python3
if __debug__:
    from EmulatorGUI import GPIO
else:
    from RPi import GPIO

import time
from logger import setup_logger


def Main():
    try:
        logger = setup_logger('blink.py')

        logger.info('Starting blink program')
        chan_list = (17, 27, 22)

        logger.info('Setting up GPIO')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(chan_list[0], GPIO.OUT, initial=GPIO.LOW)  # Green
        GPIO.setup(chan_list[1], GPIO.OUT, initial=GPIO.LOW)  # Red
        GPIO.setup(chan_list[2], GPIO.OUT, initial=GPIO.LOW)  # Yellow
        while (True):
            GPIO.output(chan_list[0], not GPIO.input(chan_list[0]))
            time.sleep(1)
            GPIO.output(chan_list[1], not GPIO.input(chan_list[1]))
            time.sleep(1)
            GPIO.output(chan_list[2], not GPIO.input(chan_list[2]))
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        logger.info('Finishing up')
        GPIO.cleanup()


Main()
