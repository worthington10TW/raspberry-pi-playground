#!/usr/bin/env python3

import unittest
import json
from app.ci_gateway import github


class GithubTests(unittest.TestCase):
    def test_map_result(self):
        latest = """{
            "id": 448533827,
            "status": "completed",
            "conclusion": "success",
            "created_at": "2020-12-28T09:23:57Z"
        }"""
        result = github.GitHubAction.map_result(json.loads(latest))
        self.assertEqual("GITHUB", result["type"])
        self.assertEqual("PASS", result["status"])
        self.assertEqual("2020-12-28T09:23:57Z", result["start"])
        self.assertEqual(448533827, result["id"])


if __name__ == '__main__':
    unittest.main()
