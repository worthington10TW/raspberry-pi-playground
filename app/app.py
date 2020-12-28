#!/usr/bin/env python3

from log_handler import setup_logger
import gpio.setup_board as board
import gpio.board_constants as pins
from gpio.light import Light
from time import sleep
import logging
import asyncio


def main():
    setup_logger()
    logging.info("Hello World!")

    with board.SetupBoard((
            pins.GREEN, pins.YELLOW, pins.RED, pins.BLUE)):
        green = Light(pins.GREEN)

        while True:
            green.on()
            sleep(1)
            green.off()
            sleep(1)
            green.off()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
