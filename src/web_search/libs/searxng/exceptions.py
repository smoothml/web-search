class SearxngClientError(Exception):
    """Base exception for SearXNG client failures."""


class SearxngTransportError(SearxngClientError):
    """Raised when an HTTP request to SearXNG fails."""


class SearxngResponseError(SearxngClientError):
    """Raised when a SearXNG response payload cannot be parsed."""
