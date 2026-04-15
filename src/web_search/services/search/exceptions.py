class SearchServiceError(Exception):
    """Base exception for search service failures."""


class SearchServiceClientError(SearchServiceError):
    """Raised when the underlying search client fails."""
