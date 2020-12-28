#!/usr/bin/env python3

import logging
import asyncio
import json
import os
import gpio.setup_board as board
import gpio.board_constants as pins
from ci_gateway.constants import Result
import aggregator_service as s
import integration_mapper as m

from log_handler import setup_logger
from gpio.light import Light, Pulse, LightWrapper
from time import sleep


def main():
    setup_logger()
    logging.info("Hello World!")

    service = s.AggregatorService(get_integrations())

    with board.SetupBoard((
            pins.GREEN, pins.YELLOW, pins.RED, pins.BLUE)):
        green = Light(pins.GREEN)
        red = Light(pins.RED)
        yellow = Pulse(pins.YELLOW)
        blue = Light(pins.BLUE)

        while True:
            with LightWrapper(pins.BLUE):
                blue.on()
                result = service.run()
                status = result['status']
                # is_running = result['is_running']
                blue.off()

            if status == Result.PASS:
                green.on()
                red.off()
            elif status == Result.FAIL:
                green.off()
                red.on()
            else:
                green.on()
                red.on()

            yellow.start()
            # yellow.start() if is_running else yellow.stop()

            sleep(10)


def get_integrations():
    RESPONSE_JSON = os.path.join(
        os.path.dirname(__file__),
        'integrations.conf')
    with open(RESPONSE_JSON) as integrations:
        data = json.load(integrations)

    return m.IntegrationMapper(data).get()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
