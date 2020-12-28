#!/usr/bin/env python3

from app.ci_gateway.constants import Result


def get_status(result):
    print(result)
    if any(r['status'] == Result.FAIL for r in result):
        return Result.FAIL

    elif all(r['status'] == Result.PASS for r in
             filter(lambda x: x['status'] != Result.RUNNING, result)):
        return Result.PASS
    else:
        return Result.UNKNOWN


class AggregatorService(object):
    def __init__(self, integrations):
        self.integrations = integrations

    def run(self):
        result = []
        for i in self.integrations:
            result.append(i['action']())

        return dict(
            type="AGGREGATED",
            start=None,
            is_running=True
            if any(r['status'] == Result.RUNNING for r in result)
            else False,
            status=get_status(result))
