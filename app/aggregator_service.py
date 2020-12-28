#!/usr/bin/env python3

import ci_gateway.constants as r


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
            status=r.Result.PASS)
