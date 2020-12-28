#!/usr/bin/env python3

import app.ci_gateway.constants as r


class AggregatorService(object):
    def __init__(self, integrations):
        self.integrations = integrations

    def get(self):
        return dict(
            type="AGGREGATED",
            start=None,
            status=r.Result.PASS)
