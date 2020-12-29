#!/usr/bin/env python3

import unittest

from src.service.aggregator_service import Result, AggregatorService
import src.ci_gateway.constants as github_constants


def return_pass():
    return dict(status=github_constants.Result.PASS)


def return_fail():
    return dict(status=github_constants.Result.FAIL)


def return_running():
    return dict(status=github_constants.Result.RUNNING)


class GithubTests(unittest.TestCase):

    def test_is_running(self):
        actions = [
            {"action": return_pass},
            {"action": return_fail},
            {"action": return_running}
        ]
        result = AggregatorService(actions).run()
        self.assertEqual(True, result["is_running"])

    def test_is_not_running(self):
        actions = [
            {"action": return_pass},
            {"action": return_fail}
        ]
        result = AggregatorService(actions).run()
        self.assertEqual(False, result["is_running"])

    def test_contains_failed(self):
        actions = [
            {"action": return_pass},
            {"action": return_fail},
        ]
        result = AggregatorService(actions).run()
        self.assertEqual(Result.FAIL, result["status"])

    def test_all_pass(self):
        actions = [
            {"action": return_pass},
            {"action": return_pass},
            {"action": return_running},
        ]
        result = AggregatorService(actions).run()
        self.assertEqual(Result.PASS, result["status"])

    def test_no_results(self):
        actions = [
            {"action": return_running}
        ]
        result = AggregatorService(actions).run()
        self.assertEqual(Result.NONE, result["status"])


if __name__ == '__main__':
    unittest.main()
