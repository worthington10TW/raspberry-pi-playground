#!/usr/bin/env python3

import pytest
import json
import os
import aiounittest
from aioresponses import aioresponses

from src.ci_gateway.circleci import CircleCI, APIError
from src.ci_gateway.constants import Result, Integration

os.environ['CIRCLECI_TOKEN'] = 'secret'


class CircleCiTests(aiounittest.AsyncTestCase):
    def test_map_result(self):
        latest = """{
            "build_num": 1234,
            "outcome": "success",
            "lifecycle": "finished",
            "start_time": "2020-12-28T09:23:57Z"
        }"""
        result = CircleCI.map_result(json.loads(latest))
        self.assertEqual(Integration.CIRCLECI, result["type"])
        self.assertEqual(Result.PASS, result["status"])
        self.assertEqual("2020-12-28T09:23:57Z", result["start"])
        self.assertEqual(1234, result["id"])

    def test_running(self):
        latest = """{
                    "build_num": 1234,
                    "outcome": "failed",
                    "lifecycle": "not_finished",
                    "start_time": "2020-12-28T09:23:57Z"
                }"""
        result = CircleCI.map_result(json.loads(latest))
        self.assertEqual(Result.RUNNING, result["status"])

    def test_pass(self):
        latest = """{
                    "build_num": 1234,
                    "outcome": "success",
                    "lifecycle": "finished",
                    "start_time": "2020-12-28T09:23:57Z"
                }"""
        result = CircleCI.map_result(json.loads(latest))
        self.assertEqual(Result.PASS, result["status"])

    def test_failed(self):
        latest = """{
                    "build_num": 1234,
                    "outcome": "failed",
                    "lifecycle": "finished",
                    "start_time": "2020-12-28T09:23:57Z"
                }"""
        result = CircleCI.map_result(json.loads(latest))
        self.assertEqual(Result.FAIL, result["status"])

    @aioresponses()
    async def test_gets_latest_from_git(self, m):
        RESPONSE_JSON = os.path.join(
            os.path.dirname(__file__),
            'circleci_response.json')
        with open(RESPONSE_JSON) as json_file:
            data = json.load(json_file)

        m.get('https://circleci.com/api/v1.1/project/github/super-man/awesome?limit=1&shallow=true',  # noqa: E501
              payload=data, status=200)

        action = CircleCI('super-man', 'awesome')
        result = await action.get_latest()
        self.assertEqual(Integration.CIRCLECI, result["type"])
        self.assertEqual(Result.PASS, result["status"])

    @aioresponses()
    async def test_fails_when_not_200(self, m):
        with pytest.raises(APIError) as excinfo:
            m.get(
                'https://circleci.com/api/v1.1/project/github/super-man/awesome?limit=1&shallow=true',  # noqa: E501
                status=400)
            action = CircleCI('super-man', 'awesome')
            await action.get_latest()

        msg = "APIError: GET https://circleci.com/api/v1.1/project/github/super-man/awesome?limit=1&shallow=true 400"  # noqa: E501
        self.assertEqual(msg, str(excinfo.value))


if __name__ == '__main__':
    aiounittest.main()
