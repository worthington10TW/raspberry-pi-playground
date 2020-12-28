#!/usr/bin/env python3

import unittest
import pytest
import json
import requests_mock
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

    def test_running(self):
        latest = """{
            "id": 448533827,
            "status": "in_progress",
            "conclusion": null,
            "created_at": "2020-12-28T09:23:57Z"
        }"""
        result = github.GitHubAction.map_result(json.loads(latest))
        self.assertEqual("RUNNING", result["status"])

    def test_queued(self):
        latest = """{
            "id": 448533827,
            "status": "queued",
            "conclusion": null,
            "created_at": "2020-12-28T09:23:57Z"
        }"""
        result = github.GitHubAction.map_result(json.loads(latest))
        self.assertEqual("RUNNING", result["status"])

    def test_pass(self):
        latest = """{
            "id": 448533827,
            "status": "completed",
            "conclusion": "success",
            "created_at": "2020-12-28T09:23:57Z"
        }"""
        result = github.GitHubAction.map_result(json.loads(latest))
        self.assertEqual("PASS", result["status"])


    def test_failed(self):
        latest = """{
            "id": 448533827,
            "status": "completed",
            "conclusion": "failure",
            "created_at": "2020-12-28T09:23:57Z"
        }"""
        result = github.GitHubAction.map_result(json.loads(latest))
        self.assertEqual("FAIL", result["status"])

    def test_unknown_not_completed(self):
        latest = """{
            "id": 448533827,
            "status": "something",
            "conclusion": null,
            "created_at": "2020-12-28T09:23:57Z"
        }"""
        result = github.GitHubAction.map_result(json.loads(latest))
        self.assertEqual("UNKNOWN", result["status"])

    def test_unknown_not_completed(self):
        latest = """{
            "id": 448533827,
            "status": "something",
            "conclusion": "completed",
            "created_at": "2020-12-28T09:23:57Z"
        }"""
        result = github.GitHubAction.map_result(json.loads(latest))
        self.assertEqual("UNKNOWN", result["status"])

    @requests_mock.Mocker()
    def test_gets_latest_from_git(self, m):
        with open('response.json') as json_file:
            data = json.load(json_file)
            m.get('https://api.github.com/repos/super-man/awesome/actions/runs', json=data, status_code=200)
            result = github.GitHubAction('super-man', 'awesome').get_latest()
            self.assertEqual("GITHUB", result["type"])
            self.assertEqual("FAIL", result["status"])

    @requests_mock.Mocker()
    def test_fails_when_not_200(self, m):
        with pytest.raises(github.APIError) as excinfo:
            m.get('https://api.github.com/repos/super-man/awesome/actions/runs', json={}, status_code=400)
            github.GitHubAction('super-man', 'awesome').get_latest()
        self.assertEqual("APIError: GET https://api.github.com/repos/super-man/awesome/actions/runs 400", str(excinfo.value))

if __name__ == '__main__':
    unittest.main()
