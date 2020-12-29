#!/usr/bin/env python3

import logging
import asyncio
import json
import os
import gpio.setup_board as board
import gpio.board_constants as pins
from service.aggregator_service import AggregatorService, Result
from service.integration_mapper import IntegrationMapper
import time

from log_handler import setup_logger
from gpio.light import Light, Pulse, LightWrapper


def main():
    setup_logger()
    logging.info("Hello World!")

    aggregator = AggregatorService(get_integrations())

    with board.SetupBoard((
            pins.GREEN, pins.YELLOW, pins.RED, pins.BLUE)):
        green = Light(pins.GREEN)
        red = Light(pins.RED)
        yellow = Pulse(pins.YELLOW)
        blue = Light(pins.BLUE)

        while True:
            with LightWrapper(pins.BLUE):
                blue.on()
                result = aggregator.run()
                status = result['status']
                is_running = result['is_running']
                blue.off()

            if status == Result.PASS:
                green.on()
                red.off()
            elif status == Result.FAIL:
                green.off()
                red.on()
            elif status == Result.UNKNOWN:
                green.on()
                red.on()
            else:
                green.off()
                red.off()

            yellow.on() if is_running else yellow.off()

            time.sleep(10)


def get_integrations():
    RESPONSE_JSON = os.path.join(
        os.path.dirname(__file__),
        'integrations.conf')
    with open(RESPONSE_JSON) as integrations:
        data = json.load(integrations)

    return IntegrationMapper(data).get()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
