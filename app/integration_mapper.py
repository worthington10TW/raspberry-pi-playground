#!/usr/bin/env python3

from app.ci_gateway import constants as c
from app.ci_gateway import github


def _map_git(username, repo):
    action = github.GitHubAction(username, repo)
    return action.get_latest


def _map(integration):
    action = {
        c.Integration.GITHUB: _map_git(integration['username'],
                                       integration['repo']),
    }
    return {
        'type': c.Integration[integration['type']],
        'action': action.get(c.Integration[integration['type']])
    }


class IntegrationMapper(object):
    def __init__(self, integrations, pin):
        self.integrations = integrations
        self.pin = pin
        self.__validate_integrations()

    def __validate_integrations(self):
        valid_integrations = set(item.value for item in c.Integration)

        for i in self.integrations:
            if i['type'] not in valid_integrations:
                raise MismatchError(i['type'])

    def get(self):
        return list(map(_map, self.integrations))


class MismatchError(Exception):
    """An Integration Error Exception"""

    def __init__(self, integration):
        self.integration = integration

    def __str__(self):
        return f'Integration error: we currently do not integrate with {self.integration}.'  # noqa: E501
