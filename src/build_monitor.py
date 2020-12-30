#!/usr/bin/env python3

import logging
from src.gpio.constants import Lights
from src.service.aggregator_service import AggregatorService, Result


class BuildMonitor(object):
    def __init__(self,
                 board,
                 aggregator: AggregatorService):
        self.board = board
        self.aggregator = aggregator

    async def run(self):
        self.board.on(Lights.BLUE)
        logging.info("Getting build results")
        result = await self.aggregator.run()
        status = result['status']
        is_running = result['is_running']
        self.board.off(Lights.BLUE)

        logging.info("Setting output")
        if status == Result.PASS:
            self.board.on(Lights.GREEN)
            self.board.off(Lights.RED)
        elif status == Result.FAIL:
            self.board.off(Lights.GREEN)
            self.board.on(Lights.RED)
        elif status == Result.UNKNOWN:
            self.board.on(Lights.GREEN)
            self.board.on(Lights.RED)
        else:
            self.board.off(Lights.GREEN)
            self.board.off(Lights.RED)

        if is_running:
            await self.board.pulse(Lights.YELLOW)
        else:
            self.board.off(Lights.YELLOW)

        logging.info("Finished build run")