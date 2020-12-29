#!/usr/bin/env python3

import logging
import asyncio
import json
import os
from gpio.board import Board
from gpio.constants import Lights
from service.aggregator_service import AggregatorService, Result
from service.integration_mapper import IntegrationMapper
import time

from log_handler import setup_logger


def main():
    setup_logger()
    logging.info("Hello World!")

    aggregator = AggregatorService(get_integrations())

    with Board() as board:
        while True:
            board.on(Lights.BLUE)
            result = aggregator.run()
            status = result['status']
            is_running = result['is_running']
            board.off(Lights.BLUE)

            if status == Result.PASS:
                board.on(Lights.GREEN)
                board.off(Lights.RED)
            elif status == Result.FAIL:
                board.off(Lights.GREEN)
                board.on(Lights.RED)
            elif status == Result.UNKNOWN:
                board.on(Lights.GREEN)
                board.on(Lights.RED)
            else:
                board.off(Lights.GREEN)
                board.off(Lights.RED)

            board.pulse(Lights.YELLOW) \
                if is_running \
                else board.off(Lights.YELLOW)

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
