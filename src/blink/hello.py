#!/usr/bin/python3

from time import sleep
from logger import setup_logger


def Main():
    try:
        logger = setup_logger('hello.py')
        logger.info('Starting hello program')
        while True:
            logger.info("I'm here!")
            sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        logger.info('Finishing up')


Main()
