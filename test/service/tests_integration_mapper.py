#!/usr/bin/env python3

import unittest
import pytest
from unittest import mock

import src.ci_gateway.constants as cons
from src.service.integration_mapper import IntegrationMapper, MismatchError


class IntegrationMapperTests(unittest.TestCase):
    def test_fails_when_integration_is_unknown(self):
        integrations = [
            {
                'type': 'BLURGH',
                'username': 'meee',
                'repo': 'super-repo'
            }
        ]
        with pytest.raises(MismatchError) as excinfo:
            IntegrationMapper(integrations, 1)

        msg = 'Integration error: we currently do not integrate with BLURGH.'  # noqa: E501
        self.assertEqual(msg, str(excinfo.value))

    def test_maps_correct_function(self):
        integrations = [
            {
                'type': 'GITHUB',
                'username': 'meee',
                'repo': 'super-repo'
            },
            {
                'type': 'GITHUB',
                'username': 'you',
                'repo': 'another-repo'
            }
        ]
        result = IntegrationMapper(integrations, 1).get()
        self.assertEqual(2, len(result))
        [self.assertEqual(cons.Integration.GITHUB, r['type']) for r in result]
        [self.assertIsNotNone(r['action']) for r in result]

    @mock.patch('src.ci_gateway.github.GitHubAction')
    def test_executes_correct_function(self, mocked):
        integrations = [
            {
                'type': 'GITHUB',
                'username': 'meee',
                'repo': 'super-repo'
            },
            {
                'type': 'GITHUB',
                'username': 'you',
                'repo': 'another-repo'
            }
        ]
        mocked.return_value.get_latest = mock.MagicMock()

        result = IntegrationMapper(integrations, 1).get()

        self.assertEqual(2, mocked.call_count)
        self.assertEqual(mock.call('meee', 'super-repo'),
                         mocked.call_args_list[0])
        self.assertEqual(mock.call('you', 'another-repo'),
                         mocked.call_args_list[1])

        mocked.return_value.get_latest.assert_not_called()
        result[0]['action']()
        self.assertEqual(1, mocked.return_value.get_latest.call_count)
        result[1]['action']()
        self.assertEqual(2, mocked.return_value.get_latest.call_count)

        # Asserting that setup is only called once
        self.assertEqual(2, mocked.call_count)


if __name__ == '__main__':
    unittest.main()