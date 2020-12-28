#!/usr/bin/env python3

from enum import Enum


class Result(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    RUNNING = "RUNNING"
    UNKNOWN = "UNKNOWN"


class Integration(Enum):
    GITHUB = "GITHUB"
