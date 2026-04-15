from unittest.mock import MagicMock

import pytest
import requests
from pydantic import HttpUrl

from web_search.libs.searxng.exceptions import (
    SearxngResponseError,
    SearxngTransportError,
)
from web_search.libs.searxng.client import SearxngClient


@pytest.fixture(scope="function")
def requests_get_mock(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Patch the requests.get lookup used by SearxngClient."""
    get_mock = MagicMock()
    monkeypatch.setattr("web_search.libs.searxng.client.requests.get", get_mock)
    return get_mock


@pytest.mark.parametrize(
    "base_url",
    [
        "http://localhost:8080",
        "http://localhost:8080/",
    ],
)
def test_search_builds_expected_request(
    base_url: str,
    requests_get_mock: MagicMock,
) -> None:
    """search() should call /search with query and JSON format params."""
    requests_get_mock.return_value.raise_for_status.return_value = None
    requests_get_mock.return_value.json.return_value = {"results": []}

    client = SearxngClient(base_url=HttpUrl(base_url))
    client.search("python testing")

    requests_get_mock.assert_called_once_with(
        "http://localhost:8080/search",
        params={"q": "python testing", "format": "json"},
        timeout=10.0,
    )


def test_search_returns_parsed_results(requests_get_mock: MagicMock) -> None:
    """search() should parse result items into Pydantic models."""
    requests_get_mock.return_value.raise_for_status.return_value = None
    requests_get_mock.return_value.json.return_value = {
        "results": [
            {
                "url": "https://example.com/a",
                "title": "A",
                "content": "Alpha",
            },
            {
                "url": "https://example.com/b",
                "title": "B",
                "content": "Beta",
            },
        ]
    }

    client = SearxngClient(base_url=HttpUrl("http://localhost:8080"))
    results = client.search(query="example", num_results=2)

    assert results.query == "example"
    assert results.num_results == 2
    assert str(results.results[0].url) == "https://example.com/a"
    assert results.results[1].title == "B"


def test_search_limits_results_to_num_results(requests_get_mock: MagicMock) -> None:
    """search() should limit returned items to num_results."""
    requests_get_mock.return_value.raise_for_status.return_value = None
    requests_get_mock.return_value.json.return_value = {
        "results": [
            {
                "url": "https://example.com/1",
                "title": "One",
                "content": "First",
            },
            {
                "url": "https://example.com/2",
                "title": "Two",
                "content": "Second",
            },
        ]
    }

    client = SearxngClient(base_url=HttpUrl("http://localhost:8080"))
    results = client.search(query="example", num_results=1)

    assert results.num_results == 1
    assert str(results.results[0].url) == "https://example.com/1"


def test_search_raises_for_invalid_num_results() -> None:
    """search() should reject non-positive num_results values."""
    client = SearxngClient(base_url=HttpUrl("http://localhost:8080"))

    with pytest.raises(ValueError, match="num_results"):
        client.search(query="example", num_results=0)


def test_search_raises_transport_error_on_request_failure(
    requests_get_mock: MagicMock,
) -> None:
    """search() should raise SearxngTransportError for transport failures."""
    requests_get_mock.side_effect = requests.Timeout("Timed out")

    client = SearxngClient(base_url=HttpUrl("http://localhost:8080"))

    with pytest.raises(SearxngTransportError):
        client.search("example")


def test_search_raises_transport_error_on_http_status(
    requests_get_mock: MagicMock,
) -> None:
    """search() should raise SearxngTransportError for HTTP status failures."""
    requests_get_mock.return_value.raise_for_status.side_effect = requests.HTTPError(
        "HTTP failure"
    )

    client = SearxngClient(base_url=HttpUrl("http://localhost:8080"))

    with pytest.raises(SearxngTransportError):
        client.search("example")


def test_search_raises_response_error_for_invalid_json(
    requests_get_mock: MagicMock,
) -> None:
    """search() should raise SearxngResponseError for invalid JSON."""
    requests_get_mock.return_value.raise_for_status.return_value = None
    requests_get_mock.return_value.json.side_effect = ValueError("Invalid JSON")

    client = SearxngClient(base_url=HttpUrl("http://localhost:8080"))

    with pytest.raises(SearxngResponseError):
        client.search("example")


def test_search_raises_response_error_for_missing_results_field(
    requests_get_mock: MagicMock,
) -> None:
    """search() should raise SearxngResponseError when results are missing."""
    requests_get_mock.return_value.raise_for_status.return_value = None
    requests_get_mock.return_value.json.return_value = {"answers": []}

    client = SearxngClient(base_url=HttpUrl("http://localhost:8080"))

    with pytest.raises(SearxngResponseError):
        client.search("example")


def test_search_raises_response_error_for_invalid_payload(
    requests_get_mock: MagicMock,
) -> None:
    """search() should raise SearxngResponseError for schema mismatches."""
    requests_get_mock.return_value.raise_for_status.return_value = None
    requests_get_mock.return_value.json.return_value = {
        "results": [
            {
                "url": "https://example.com/1",
                "title": "One",
            }
        ]
    }

    client = SearxngClient(base_url=HttpUrl("http://localhost:8080"))

    with pytest.raises(SearxngResponseError):
        client.search("example")
