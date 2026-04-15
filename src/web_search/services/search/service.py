from typing import Protocol

from web_search.libs.searxng.exceptions import SearxngClientError
from web_search.schemas import SearchResults
from web_search.services.search.exceptions import SearchServiceClientError


class SearchClient(Protocol):
    def search(self, query: str, num_results: int) -> SearchResults:
        """Get web search results.

        Args:
            query: Search query.
            num_results: Maximum number of results to return.

        Returns:
            A SearchResults instance containing the results.
        """
        ...


class SearchService:
    """Search service."""

    def __init__(self, client: SearchClient) -> None:
        """Initialise search service."""
        self._client = client

    def search(self, query: str, num_results: int = 10) -> SearchResults:
        """Run a web search.

        Args:
            query: Search query.
            num_results: Maximum number of results to return.

        Returns:
            A SearchResults instance containing the results.

        Raises:
            ValueError: If query is blank or num_results is not positive.
            SearchServiceClientError: If the search client fails.
        """
        if not query.strip():
            raise ValueError("query must not be empty.")

        if num_results <= 0:
            raise ValueError("num_results must be greater than 0.")

        try:
            return self._client.search(query, num_results)
        except SearxngClientError as exc:
            raise SearchServiceClientError("Search client failed.") from exc
