#!/usr/bin/env python3

import enum


class Result(enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    RUNNING = "RUNNING"
    UNKNOWN = "UNKNOWN"
    NONE = "NONE"


class Integration(enum.Enum):
    GITHUB = "GITHUB"
    CIRCLECI = "CIRCLE_CI"


class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, verb, url, status):
        self.verb = verb
        self.url = url
        self.status = status

    def __str__(self):
        return f'APIError: {self.verb} {self.url} {self.status}'
