from aiohttp import ClientResponse

from ..exc.http import (
    HttpRequestException,
    WebsiteDownException,
    WebsiteDomainMovedException,
    WebsiteRedirectException,
    EndpointNotFoundException,
    ResourceUnavailableException
)


def raise_http_exception(response: ClientResponse):
    if response.status == 500:
        raise_http_website_down_exception(response)

    if response.status == 404:
        raise_http_endpoint_not_found_exception(response)

    if response.status in [401, 403]:
        raise_http_resource_unavailable_exception(response)

    if str(response.status).startswith('3'):
        raise_http_website_domain_moved_exception(response)

    raise HttpRequestException("Unknown http exception", response)


def raise_http_website_down_exception(response: ClientResponse):
    raise WebsiteDownException("Website is downed now or has problem with http requests resolving", response)


def raise_http_website_domain_moved_exception(response: ClientResponse):
    raise WebsiteDomainMovedException("Website has domain drive", response)


def raise_http_website_redirected_exception(response: ClientResponse):
    raise WebsiteRedirectException("Website send redirect", response)


def raise_http_endpoint_not_found_exception(response: ClientResponse):
    raise EndpointNotFoundException("Endpoint was not found to parse", response)


def raise_http_resource_unavailable_exception(response: ClientResponse):
    raise ResourceUnavailableException("Resource are unavailable", response)
