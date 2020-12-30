import sys
import os
import logging
import asyncio
from src.ci_gateway.constants import Integration, Result
from aiohttp import ClientSession
from src.ci_gateway.api_error import APIError


class CircleCI(object):
    def __init__(self, username, repo):
        self.username = username
        self.repo = repo
        self.token = os.getenv('CIRCLE_CI_TOKEN')

    async def get_latest(self):
        base = 'https://circleci.com/api/v1.1'
        url = f'{base}/project/github/{self.username}/{self.repo}?limit=1&shallow=true'  # noqa: E501
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

        # TODO Currently takes the top job result, not the top unique job
        latest = json[0]
        response = CircleCI.map_result(latest)
        logging.info(f'Called {url}')
        logging.info(f'Response {response}')
        return response

    @staticmethod
    def map_result(latest):
        outcome = latest["outcome"]
        lifecycle = latest["lifecycle"]
        return dict(
            type=Integration.CIRCLECI,
            id=latest["build_num"],
            start=latest["start_time"],
            status=Result.RUNNING if lifecycle != "finished" else
            Result.FAIL if outcome != "success" else  # noqa: E501
            Result.PASS)


if __name__ == "__main__":
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(screen_handler)

    loop = asyncio.get_event_loop()
    task = CircleCI(sys.argv[1], sys.argv[2]).get_latest()
    done, pending = loop.run_until_complete(asyncio.wait((task,)))
    for future in done:
        value = future.result()
        print(value)
