import functools
import logging
import sys

import requests
import ujson

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %X',
)


def log_request(func):
    logger = logging.getLogger(__name__)

    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        logger.debug(f'request url: {kwargs.get("url")!r}')
        resp: requests.Response = func(*args, **kwargs)
        logger.debug(f'request headers: {ujson.dumps(dict(resp.request.headers))}')

        if body := resp.request.body:
            logger.debug(f'request body: {body.decode()}')

        logger.debug(f'status code: {resp.status_code}')
        logger.debug(f'response headers: {resp.headers}')
        logger.debug(f'response body: {resp.text}')
        return resp

    return _wrapper
