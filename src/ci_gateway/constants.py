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
