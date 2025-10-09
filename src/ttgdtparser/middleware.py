import logging
import time

from aiohttp import ClientRequest, ClientHandlerType, ClientResponse, ClientSSLError, ClientError

from ttgdtparser.exc.http import HttpRequestException
from ttgdtparser.exc.solvers import raise_http_exception


async def logging_middleware(request: ClientRequest, handler: ClientHandlerType):
    logger = logging.getLogger(__name__)

    logger.debug(f'{"=" * 20} Sent request: {request.method} {request.url} {"=" * 20}')

    try:
        start_time = time.time()
        response = await handler(request)
        elapsed = time.time() - start_time

        logger.debug(
            f'{"=" * 20} Received response: {response.status} '
            f'({elapsed:.2f}s) for {request.method} {request.url} {"=" * 20}'
        )
        return response

    except HttpRequestException as e:
        logger.debug(f'HttpRequestException: {e} for {request.method} {request.url}')
        raise e
    except ClientError as e:
        logger.error(f'ClientError: {e} for {request.method} {request.url}')
        raise e
    except Exception as e:
        logger.error(f'Unexpected error: {e} for {request.method} {request.url}')
        raise e


async def validate_response_middleware(request: ClientRequest, handler: ClientHandlerType) -> ClientResponse:
    response = await handler(request)

    if response.status != 200:
        raise_http_exception(response)

    return response
