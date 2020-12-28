import requests
import sys
from app.ci_gateway import constants as c


class GitHubAction(object):
    def __init__(self, username, repo):
        self.username = username
        self.repo = repo

    def get_latest(self):
        base = 'https://api.github.com'
        url = f'{base}/repos/{self.username}/{self.repo}/actions/runs'
        resp = requests.get(url)
        if resp.status_code != 200:
            raise APIError('GET', url, resp.status_code)

        latest = resp.json()['workflow_runs'][0]

        return GitHubAction.map_result(latest)

    @staticmethod
    def map_result(latest):
        conclusion = latest["conclusion"]
        status = latest["status"]
        return dict(
            type=c.Integration.GITHUB,
            id=latest["id"],
            start=latest["created_at"],
            status=c.Result.FAIL if status == "completed" and conclusion == "failure" else  # noqa: E501
            c.Result.PASS if status == "completed" and conclusion == "success" else  # noqa: E501
            c.Result.RUNNING if conclusion is None and (status == "queued" or status == "in_progress") else  # noqa: E501
            c.Result.UNKNOWN)


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
