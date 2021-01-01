#!/usr/bin/env python3

import logging
import asyncio
import json
import os
import pprint
from gpio.board import Board
from service.aggregator_service import AggregatorService
from service.integration_mapper import IntegrationMapper
from ci_gateway import integrations as available_integrations
from log_handler import setup_logger
from src.build_monitor import BuildMonitor


async def main(level):
    config = get_config()
    setup_logger(level)
    logging.info('Hello build monitor!')

    with Board() as board:
        logging.info('Board initialised')
        poll_in_seconds = config.get('poll_in_seconds') or 30
        integrations = config['integrations']
        logging.info(f'Polling increment (in seconds): {poll_in_seconds}')
        logging.info(f'Integrations: {pprint.pformat(integrations)}')

        aggregator = AggregatorService(
            IntegrationMapper(
                available_integrations.get_all()).get(
                integrations))
        monitor = BuildMonitor(board, aggregator)
        while True:
            await monitor.run()
            await asyncio.sleep(poll_in_seconds)


def get_config():
    response_json = os.path.join(
        os.path.dirname(__file__),
        'integrations.conf')
    with open(response_json) as integrations:
        return json.load(integrations)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-log',
        default='info',
        help=(
            'Provide logging level. '
            'Example --log debug\', default=\'warning\''),
    )

    options = parser.parse_args()
    levels = dict(critical=logging.CRITICAL,
                  error=logging.ERROR,
                  warn=logging.WARNING,
                  warning=logging.WARNING,
                  info=logging.INFO,
                  debug=logging.DEBUG)
    level = levels.get(options.log.lower())
    if level is None:
        raise ValueError(
            f'log level given: {options.log}'
            f' -- must be one of: {" | ".join(levels.keys())}')

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(level))
    except KeyboardInterrupt:
        pass
