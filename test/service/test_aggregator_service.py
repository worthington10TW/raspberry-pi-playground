#!/usr/bin/env python3

import aiounittest

from src.service.aggregator_service import Result, AggregatorService
import src.ci_gateway.constants as github_constants


async def return_pass():
    return dict(status=github_constants.Result.PASS)


async def return_fail():
    return dict(status=github_constants.Result.FAIL)


async def return_running():
    return dict(status=github_constants.Result.RUNNING)


class GithubTests(aiounittest.AsyncTestCase):

    async def test_is_running(self):
        actions = [
            {"action": return_pass},
            {"action": return_fail},
            {"action": return_running}
        ]
        result = await AggregatorService(actions).run()
        self.assertEqual(True, result["is_running"])

    async def test_is_not_running(self):
        actions = [
            {"action": return_pass},
            {"action": return_fail}
        ]
        result = await AggregatorService(actions).run()
        self.assertEqual(False, result["is_running"])

    async def test_contains_failed(self):
        actions = [
            {"action": return_pass},
            {"action": return_fail},
        ]
        result = await AggregatorService(actions).run()
        self.assertEqual(Result.FAIL, result["status"])

    async def test_all_pass(self):
        actions = [
            {"action": return_pass},
            {"action": return_pass},
            {"action": return_running},
        ]
        result = await AggregatorService(actions).run()
        self.assertEqual(Result.PASS, result["status"])

    async def test_no_results(self):
        actions = [
            {"action": return_running}
        ]
        result = await AggregatorService(actions).run()
        self.assertEqual(Result.NONE, result["status"])


if __name__ == '__main__':
    aiounittest.main()
