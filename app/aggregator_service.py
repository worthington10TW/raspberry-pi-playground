#!/usr/bin/env python3

from ci_gateway import constants as c


def get_status(result):
    if len(result) == 0:
        return c.Result.NONE
    elif any(r['status'] == c.Result.FAIL for r in result):
        return c.Result.FAIL

    elif all(r['status'] == c.Result.PASS for r in result):
        return c.Result.PASS
    else:
        return c.Result.UNKNOWN


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
            if any(r['status'] == c.Result.RUNNING for r in result)
            else False,
            status=get_status(
                list(
                    filter(
                        lambda x: x['status'] != c.Result.RUNNING, result))))
