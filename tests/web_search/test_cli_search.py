import json

import pytest
from pydantic import HttpUrl
from typer.testing import CliRunner

from web_search import cli
from web_search.schemas import SearchResult, SearchResults
from web_search.services.search.exceptions import SearchServiceClientError
from web_search.services.search.service import SearchClient

SearchOutcome = SearchResults | ValueError | SearchServiceClientError


class StubSearchService(SearchClient):
    """Stub search service for CLI tests."""

    def __init__(self, outcome: SearchOutcome) -> None:
        """Initialise the stub with a configured outcome.

        Args:
            outcome: Return value or exception to raise from ``search``.
        """
        self._outcome = outcome
        self.calls: list[tuple[str, int]] = []

    def search(self, query: str, num_results: int = 10) -> SearchResults:
        """Record calls and return or raise the configured outcome.

        Args:
            query: Search query.
            num_results: Maximum number of results.

        Returns:
            Search results from the configured stub outcome.

        Raises:
            ValueError: If configured with a validation error.
            SearchServiceClientError: If configured with a service client error.
        """
        self.calls.append((query, num_results))
        if isinstance(self._outcome, SearchResults):
            return self._outcome
        raise self._outcome


@pytest.fixture(scope="function")
def runner() -> CliRunner:
    """Create an isolated CLI runner."""
    return CliRunner()


@pytest.fixture(scope="function")
def sample_search_results() -> SearchResults:
    """Build a sample search result payload."""
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


def test_search_renders_human_readable_output_by_default(
    runner: CliRunner,
    monkeypatch: pytest.MonkeyPatch,
    sample_search_results: SearchResults,
) -> None:
    """Search should render text output by default."""
    stub_service = StubSearchService(outcome=sample_search_results)

    monkeypatch.setattr("web_search.cli._build_search_service", lambda: stub_service)
    monkeypatch.setattr(
        "web_search.cli.render_search_results_markdown",
        lambda _: "FORMATTED",
    )

    result = runner.invoke(cli.app, ["search", "python"])

    assert result.exit_code == 0
    assert stub_service.calls == [("python", 10)]
    assert result.output == "FORMATTED\n"


def test_search_passes_num_results_option_to_service(
    runner: CliRunner,
    monkeypatch: pytest.MonkeyPatch,
    sample_search_results: SearchResults,
) -> None:
    """Search should pass the CLI num-results option to the service."""
    stub_service = StubSearchService(outcome=sample_search_results)

    monkeypatch.setattr("web_search.cli._build_search_service", lambda: stub_service)

    result = runner.invoke(cli.app, ["search", "python", "--num-results", "3"])

    assert result.exit_code == 0
    assert stub_service.calls == [("python", 3)]


def test_search_returns_json_with_json_option(
    runner: CliRunner,
    monkeypatch: pytest.MonkeyPatch,
    sample_search_results: SearchResults,
) -> None:
    """Search should serialise output as JSON when --json is provided."""
    stub_service = StubSearchService(outcome=sample_search_results)

    monkeypatch.setattr("web_search.cli._build_search_service", lambda: stub_service)

    result = runner.invoke(cli.app, ["search", "python", "--json"])

    assert result.exit_code == 0
    assert stub_service.calls == [("python", 10)]

    payload = json.loads(result.output)
    assert payload == sample_search_results.model_dump(mode="json")


def test_search_exits_with_code_1_on_service_failure(
    runner: CliRunner,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Search should return exit code 1 when the service fails."""
    stub_service = StubSearchService(
        outcome=SearchServiceClientError("Search client failed."),
    )

    monkeypatch.setattr("web_search.cli._build_search_service", lambda: stub_service)

    result = runner.invoke(cli.app, ["search", "python"])

    assert result.exit_code == 1
    assert "Search client failed." in result.output


def test_search_maps_validation_error_to_bad_parameter(
    runner: CliRunner,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Search should surface validation errors as CLI parameter errors."""
    stub_service = StubSearchService(outcome=ValueError("query must not be empty."))

    monkeypatch.setattr("web_search.cli._build_search_service", lambda: stub_service)

    result = runner.invoke(cli.app, ["search", "   "])

    assert result.exit_code == 2
    assert "query must not be empty." in result.output


def test_search_rejects_non_positive_num_results_option(runner: CliRunner) -> None:
    """Search should reject non-positive --num-results values at the CLI layer."""
    result = runner.invoke(cli.app, ["search", "python", "--num-results", "0"])

    assert result.exit_code == 2
    assert "Invalid value for '--num-results'" in result.output
