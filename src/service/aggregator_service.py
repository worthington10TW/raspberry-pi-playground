#!/usr/bin/env python3

import enum
import src.ci_gateway.constants as ci_constants


def get_status(result):
    if len(result) == 0:
        return Result.NONE
    elif any(r['status'] == ci_constants.Result.FAIL for r in result):
        return Result.FAIL

    elif all(r['status'] == ci_constants.Result.PASS for r in result):
        return Result.PASS
    else:
        return Result.UNKNOWN


class AggregatorService(object):
    def __init__(self, integrations):
        self.integrations = integrations

    async def run(self):
        tasks = [integration['action']() for integration in self.integrations]

        result = []
        [result.append(await task) for task in tasks]

        return dict(
            type="AGGREGATED",
            start=None,
            is_running=True
            if any(r['status'] == ci_constants.Result.RUNNING for r in result)
            else False,
            status=get_status(
                list(
                    filter(
                        lambda x: x['status'] != ci_constants.Result.RUNNING,
                        result))))


class Result(enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"
    NONE = "NONE"
