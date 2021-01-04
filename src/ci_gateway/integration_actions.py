#!/usr/bin/env python3


from src.ci_gateway.circleci import CircleCI
from src.ci_gateway.github import GitHubAction
from src.ci_gateway.constants import Integration


def get_all():
    action = {
        Integration.GITHUB: GitHubAction,
        Integration.CIRCLECI: CircleCI
    }

    return dict(map((lambda x: (x, action.get(x))), Integration))
