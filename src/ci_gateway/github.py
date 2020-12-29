import sys
import os
import logging
from src.ci_gateway.constants import Integration, Result
from aiohttp import ClientSession


class GitHubAction(object):
    def __init__(self, username, repo):
        self.username = username
        self.repo = repo
        self.token = os.getenv('GITHUB_TOKEN')

    async def get_latest(self):
        base = 'https://api.github.com'
        url = f'{base}/repos/{self.username}/{self.repo}/actions/runs'

        logging.debug(f'Calling {url}')

        async with ClientSession() as session:
            resp = await session.get(
                url,
                headers={'Authorization': f'token {self.token}'})

            if resp.status != 200:
                raise APIError('GET', url, resp.status)

            json = await resp.json()
        latest = json['workflow_runs'][0]
        response = GitHubAction.map_result(latest)
        logging.info(f'Called {url}')
        logging.info(f'Response {response}')
        return response

    @staticmethod
    def map_result(latest):
        conclusion = latest["conclusion"]
        status = latest["status"]
        return dict(
            type=Integration.GITHUB,
            id=latest["id"],
            start=latest["created_at"],
            status=Result.FAIL if status == "completed" and conclusion == "failure" else  # noqa: E501
            Result.PASS if status == "completed" and conclusion == "success" else  # noqa: E501
            Result.RUNNING if conclusion is None and (status == "queued" or status == "in_progress") else  # noqa: E501
            Result.UNKNOWN)


class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, verb, url, status):
        self.verb = verb
        self.url = url
        self.status = status

    def __str__(self):
        return f'APIError: {self.verb} {self.url} {self.status}'


if __name__ == '__main__':
    print(GitHubAction(sys.argv[1], sys.argv[2])
          .get_latest())
