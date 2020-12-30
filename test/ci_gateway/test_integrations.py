#!/usr/bin/env python3

import aiounittest

from src.ci_gateway import integrations
from src.ci_gateway.constants import Integration
from src.ci_gateway.github import GitHubAction
from src.ci_gateway.circleci import CircleCI


class IntegrationsTests(aiounittest.AsyncTestCase):
    def test_get_all(self):
        result = integrations.get_all()

        assert GitHubAction is result[Integration.GITHUB]
        assert CircleCI is result[Integration.CIRCLECI]

        self.assertEqual(2, len(result))


if __name__ == '__main__':
    aiounittest.main()