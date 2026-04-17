from pydantic import HttpUrl

from web_search.formatting.search import render_search_results_markdown
from web_search.schemas import SearchResult, SearchResults


def test_render_search_results_markdown_includes_query_and_count() -> None:
    """The markdown renderer should include the query and result count."""
    search_results = SearchResults(
        query="python",
        results=[
            SearchResult(
                url=HttpUrl("https://example.com/1"),
                title="One",
                content="First",
            ),
        ],
    )

    rendered = render_search_results_markdown(search_results)

    assert "Search query: python" in rendered
    assert "Number of results: 1" in rendered


def test_render_search_results_markdown_formats_each_result_as_markdown() -> None:
    """The markdown renderer should format each entry as markdown text."""
    search_results = SearchResults(
        query="python",
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

    rendered = render_search_results_markdown(search_results)

    assert "1. [One](https://example.com/1)" in rendered
    assert "2. [Two](https://example.com/2)" in rendered
    assert "First" in rendered
    assert "Second" in rendered


def test_render_search_results_markdown_handles_empty_results() -> None:
    """The markdown renderer should clearly report when no results are found."""
    search_results = SearchResults(query="python", results=[])

    rendered = render_search_results_markdown(search_results)

    assert "Search query: python" in rendered
    assert "Number of results: 0" in rendered
    assert "No results found." in rendered
