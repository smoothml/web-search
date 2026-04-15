from pydantic import HttpUrl

from web_search.schemas import SearchResult, SearchResults


def test_num_results_matches_results_length() -> None:
    """num_results should return the number of result entries."""
    results = SearchResults(
        query="example",
        results=[
            SearchResult(
                url=HttpUrl("https://example.com/1"),
                title="One",
                content="First",
            ),
            SearchResult(
                url=HttpUrl("https://example.com/2"),
                title="Two",
                content="Second",
            ),
        ],
    )

    assert results.num_results == 2
