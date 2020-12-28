#!/usr/bin/env python3

import unittest

from app.ci_gateway import constants as r
from app import aggregator_service as s


class GithubTests(unittest.TestCase):
    def test_aggregates_responses(self):
        result = s.AggregatorService("test").get()
        self.assertEqual("AGGREGATED", result["type"])
        self.assertEqual(None, result["start"])
        self.assertEqual(r.Result.PASS, result["status"])


if __name__ == '__main__':
    unittest.main()
