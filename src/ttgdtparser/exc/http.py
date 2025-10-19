from aiohttp import ClientResponse

from ..exc.base import TtgdtWebsiteParserException


class HttpRequestException(TtgdtWebsiteParserException):
    response: ClientResponse

    def __init__(self, message: str, response: ClientResponse):
        super().__init__(message)
        self.response = response


class WebsiteDownException(HttpRequestException):
    def __init__(self, message: str, response: ClientResponse):
        super().__init__(message, response)


class WebsiteDomainMovedException(HttpRequestException):
    def __init__(self, message: str, response: ClientResponse):
        super().__init__(message, response)


class WebsiteRedirectException(HttpRequestException):
    def __init__(self, message: str, response: ClientResponse):
        super().__init__(message, response)


class EndpointNotFoundException(HttpRequestException):
    def __init__(self, message: str, response: ClientResponse):
        super().__init__(message, response)


class ResourceUnavailableException(HttpRequestException):
    def __init__(self, message: str, response: ClientResponse):
        super().__init__(message, response)
