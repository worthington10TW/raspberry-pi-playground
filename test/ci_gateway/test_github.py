#!/usr/bin/env python3

import unittest
import pytest
import json
import requests_mock
import os
from src.ci_gateway.github import GitHubAction, APIError
from src.ci_gateway.constants import Result, Integration

os.environ['GITHUB_TOKEN'] = 'secret'


class GithubTests(unittest.TestCase):
    def test_map_result(self):
        latest = """{
            "id": 448533827,
            "status": "completed",
            "conclusion": "success",
            "created_at": "2020-12-28T09:23:57Z"
        }"""
        result = GitHubAction.map_result(json.loads(latest))
        self.assertEqual(Integration.GITHUB, result["type"])
        self.assertEqual(Result.PASS, result["status"])
        self.assertEqual("2020-12-28T09:23:57Z", result["start"])
        self.assertEqual(448533827, result["id"])

    def test_running(self):
        latest = """{
            "id": 448533827,
            "status": "in_progress",
            "conclusion": null,
            "created_at": "2020-12-28T09:23:57Z"
        }"""
        result = GitHubAction.map_result(json.loads(latest))
        self.assertEqual(Result.RUNNING, result["status"])

    def test_queued(self):
        latest = """{
            "id": 448533827,
            "status": "queued",
            "conclusion": null,
            "created_at": "2020-12-28T09:23:57Z"
        }"""
        result = GitHubAction.map_result(json.loads(latest))
        self.assertEqual(Result.RUNNING, result["status"])

    def test_pass(self):
        latest = """{
            "id": 448533827,
            "status": "completed",
            "conclusion": "success",
            "created_at": "2020-12-28T09:23:57Z"
        }"""
        result = GitHubAction.map_result(json.loads(latest))
        self.assertEqual(Result.PASS, result["status"])

    def test_failed(self):
        latest = """{
            "id": 448533827,
            "status": "completed",
            "conclusion": "failure",
            "created_at": "2020-12-28T09:23:57Z"
        }"""
        result = GitHubAction.map_result(json.loads(latest))
        self.assertEqual(Result.FAIL, result["status"])

    def test_unknown_not_completed(self):
        latest = """{
            "id": 448533827,
            "status": "something",
            "conclusion": null,
            "created_at": "2020-12-28T09:23:57Z"
        }"""
        result = GitHubAction.map_result(json.loads(latest))
        self.assertEqual(Result.UNKNOWN, result["status"])

    def test_unknown_completed(self):
        latest = """{
            "id": 448533827,
            "status": "something",
            "conclusion": "completed",
            "created_at": "2020-12-28T09:23:57Z"
        }"""
        result = GitHubAction.map_result(json.loads(latest))
        self.assertEqual(Result.UNKNOWN, result["status"])

    @requests_mock.Mocker()
    def test_gets_latest_from_git(self, m):
        RESPONSE_JSON = os.path.join(
            os.path.dirname(__file__),
            'response.json')
        with open(RESPONSE_JSON) as json_file:
            data = json.load(json_file)
            m.get('https://api.github.com/repos/super-man/awesome/actions/runs',  # noqa: E501
                  json=data, status_code=200)
            result = GitHubAction('super-man', 'awesome').get_latest()
            self.assertEqual(Integration.GITHUB, result["type"])
            self.assertEqual(Result.FAIL, result["status"])

    @requests_mock.Mocker()
    def test_fails_when_not_200(self, m):
        with pytest.raises(APIError) as excinfo:
            m.get('https://api.github.com/repos/super-man/awesome/actions/runs',  # noqa: E501
                  json={}, status_code=400)
            GitHubAction('super-man', 'awesome').get_latest()

        msg = "APIError: GET https://api.github.com/repos/super-man/awesome/actions/runs 400"  # noqa: E501
        self.assertEqual(msg, str(excinfo.value))


if __name__ == '__main__':
    unittest.main()
