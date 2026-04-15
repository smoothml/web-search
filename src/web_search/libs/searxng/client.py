import requests
from pydantic import HttpUrl, TypeAdapter, ValidationError

from web_search.libs.searxng.exceptions import (
    SearxngResponseError,
    SearxngTransportError,
)
from web_search.schemas import SearchResult, SearchResults

_RESULTS_ADAPTER = TypeAdapter(list[SearchResult])


class SearxngClient:
    """Client for the SearXNG search engine."""

    def __init__(self, base_url: HttpUrl, timeout: float = 10.0) -> None:
        """Initialise the client.

        Args:
            base_url: SearXNG instance base URL.
            timeout: Request timeout in seconds.
        """
        self._base_url = base_url
        self._timeout = timeout

    @property
    def _search_url(self) -> str:
        """Get search URL.

        Returns:
            Search endpoint URL.
        """
        return f"{str(self._base_url).rstrip('/')}/search"

    def search(self, query: str, num_results: int = 10) -> SearchResults:
        """Run web search with the SearXNG search engine.

        Args:
            query: Search query.
            num_results: Maximum number of results to return.

        Returns:
            A SearchResults instance containing the results.

        Raises:
            ValueError: If num_results is not a positive integer.
            SearxngTransportError: If the request fails.
            SearxngResponseError: If the response payload is invalid.
        """
        if num_results <= 0:
            raise ValueError("num_results must be greater than 0.")

        params = {
            "q": query,
            "format": "json",
        }

        try:
            response = requests.get(
                self._search_url, params=params, timeout=self._timeout
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise SearxngTransportError("Failed to call SearXNG search API.") from exc

        try:
            response_payload = response.json()
        except ValueError as exc:
            raise SearxngResponseError(
                "Failed to parse SearXNG search response."
            ) from exc

        if not isinstance(response_payload, dict):
            raise SearxngResponseError("Failed to parse SearXNG search response.")

        if "results" not in response_payload:
            raise SearxngResponseError("Failed to parse SearXNG search response.")

        try:
            parsed_results = _RESULTS_ADAPTER.validate_python(
                response_payload["results"]
            )
        except ValidationError as exc:
            raise SearxngResponseError(
                "Failed to parse SearXNG search response."
            ) from exc

        return SearchResults(
            query=query,
            results=parsed_results[:num_results],
        )
