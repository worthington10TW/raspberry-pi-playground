import os
import logging
from itertools import groupby

from src.ci_gateway.constants import Integration, Result, APIError
from aiohttp import ClientSession


class CircleCI(object):
    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.repo = kwargs.get('repo')
        self.token = os.getenv('CIRCLE_CI_TOKEN')
        self.excluded_workflows = kwargs.get('excluded_workflows') or []

    async def get_latest(self):
        base = 'https://circleci.com/api/v1.1'
        url = f'{base}/project/github/{self.username}/{self.repo}?shallow=true'  # noqa: E501
        logging.debug(f'Calling {url}')

        async with ClientSession() as session:
            resp = await session.get(
                url,
                headers={'Circle-Token': f'{self.token}',
                         'Accept': 'application/json',
                         'Content-Type': 'application/json'})

            if resp.status != 200:
                raise APIError('GET', url, resp.status)

            json = await resp.json()

        response = list(
            map(
                CircleCI.map_result,
                self.get_unique_latest_jobs(json)))
        logging.info(f'Called {url}')
        logging.info(f'Response {response}')
        return response

    @staticmethod
    def map_result(latest):
        outcome = latest["outcome"]
        lifecycle = latest["lifecycle"]
        return dict(
            type=Integration.CIRCLECI,
            vcs=latest["vcs_url"],
            id=latest["build_num"],
            name=latest['workflows']['workflow_name'],
            start=latest["start_time"],
            status=Result.RUNNING if lifecycle != "finished" else
            Result.FAIL if outcome != "success" else  # noqa: E501
            Result.PASS)

    def get_unique_latest_jobs(self, json):
        jobs = []
        for k, g in groupby(
                sorted(
                    filter(
                        lambda x: x['workflows']['workflow_name']
                        not in self.excluded_workflows,
                        json), key=lambda x: x['workflows']['workflow_name']),
                lambda x: x['workflows']['workflow_name']):
            jobs.append(list(g)[0])

        return jobs


if __name__ == "__main__":
    import argparse
    import sys
    import asyncio

    parser = argparse.ArgumentParser()

    parser.add_argument('--username', help='repo username')
    parser.add_argument('--repo', help='repo to query')
    parser.add_argument('--excluded_workflows', help='excluded workflows')

    args = parser.parse_args()

    screen_handler = logging.StreamHandler(stream=sys.stdout)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(screen_handler)

    loop = asyncio.get_event_loop()

    args.excluded_workflows = args.excluded_workflows or []
    task = CircleCI(
        **{
            'username': args.username,
            'repo': args.repo,
            'excluded_workflows': args.excluded_workflows
        }).get_latest()
    done, pending = loop.run_until_complete(asyncio.wait((task,)))
    for future in done:
        value = future.result()
        print(value)
