from unittest.mock import MagicMock

import pytest
from pydantic import HttpUrl

from web_search.libs.searxng.exceptions import (
    SearxngResponseError,
    SearxngTransportError,
)
from web_search.schemas import SearchResult, SearchResults
from web_search.services.search.exceptions import SearchServiceClientError
from web_search.services.search.service import SearchService


@pytest.fixture(scope="function")
def sample_search_results() -> SearchResults:
    """Build a sample SearchResults payload."""
    return SearchResults(
        query="python",
        results=[
            SearchResult(
                url=HttpUrl("https://example.com/1"),
                title="One",
                content="First",
            ),
        ],
    )


@pytest.mark.parametrize(
    ("num_results", "expected_num_results"),
    [
        (None, 10),
        (5, 5),
    ],
)
def test_search_calls_client_with_expected_arguments(
    num_results: int | None,
    expected_num_results: int,
    sample_search_results: SearchResults,
) -> None:
    """search() should delegate to the client with expected arguments."""
    client_mock = MagicMock()
    client_mock.search.return_value = sample_search_results
    service = SearchService(client=client_mock)

    if num_results is None:
        result = service.search(query="python")
    else:
        result = service.search(query="python", num_results=num_results)

    assert result == sample_search_results
    client_mock.search.assert_called_once_with("python", expected_num_results)


@pytest.mark.parametrize(
    ("query", "num_results", "error_message"),
    [
        ("", 10, "query must not be empty"),
        ("   ", 10, "query must not be empty"),
        ("python", 0, "num_results must be greater than 0"),
    ],
)
def test_search_validates_inputs(
    query: str,
    num_results: int,
    error_message: str,
) -> None:
    """search() should validate user input before calling the client."""
    client_mock = MagicMock()
    service = SearchService(client=client_mock)

    with pytest.raises(ValueError, match=error_message):
        service.search(query=query, num_results=num_results)

    client_mock.search.assert_not_called()


@pytest.mark.parametrize(
    "client_error",
    [
        SearxngTransportError("Timed out"),
        SearxngResponseError("Invalid response payload"),
    ],
)
def test_search_wraps_searxng_client_errors(
    client_error: SearxngTransportError | SearxngResponseError,
) -> None:
    """search() should wrap SearXNG client failures in a service-level error."""
    client_mock = MagicMock()
    client_mock.search.side_effect = client_error
    service = SearchService(client=client_mock)

    with pytest.raises(SearchServiceClientError, match="Search client failed") as exc:
        service.search(query="python")

    assert isinstance(exc.value.__cause__, type(client_error))
