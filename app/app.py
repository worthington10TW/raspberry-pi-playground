#!/usr/bin/env python3

import logging
import asyncio
import json
import os
import gpio.setup_board as board
import gpio.board_constants as pins
import integration_mapper as mapper

from log_handler import setup_logger
from gpio.light import Light
from time import sleep


def main():
    setup_logger()
    logging.info("Hello World!")
    RESPONSE_JSON = os.path.join(
        os.path.dirname(__file__),
        'integrations.conf')
    with open(RESPONSE_JSON) as integrations:
        data = json.load(integrations)

    integrations = mapper.IntegrationMapper(data).get()
    print(integrations)

    with board.SetupBoard((
            pins.GREEN, pins.YELLOW, pins.RED)):
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
