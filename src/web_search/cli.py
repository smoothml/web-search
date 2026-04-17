import json

import typer

from web_search.formatting.search import render_search_results_markdown
from web_search.libs.searxng.client import SearxngClient
from web_search.services.search.exceptions import SearchServiceClientError
from web_search.services.search.service import SearchService
from web_search.settings import Settings

app = typer.Typer(help="Web search CLI.")


def _build_search_service() -> SearchService:
    """Build a configured search service instance.

    Returns:
        A configured ``SearchService``.
    """
    settings = Settings()
    client = SearxngClient(base_url=settings.searxng_base_url)
    return SearchService(client=client)


@app.command()
def search(
    query: str,
    num_results: int = typer.Option(
        10,
        "--num-results",
        "-n",
        min=1,
        help="Maximum number of search results to return.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Return search results as JSON.",
    ),
) -> None:
    """Run a web search.

    Args:
        query: Search query string.
        num_results: Maximum number of results to return.
        json_output: Output JSON when true.

    Raises:
        typer.BadParameter: If query validation fails.
        typer.Exit: If the search service fails.
    """
    service = _build_search_service()

    try:
        search_results = service.search(query=query, num_results=num_results)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    except SearchServiceClientError as exc:
        typer.echo(f"Search error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    if json_output:
        typer.echo(json.dumps(search_results.model_dump(mode="json")))
        return

    typer.echo(render_search_results_markdown(search_results))


@app.command()
def get_content(url: str) -> None:
    """Get website content converted to markdown format (best effort).

    Args:
        url: URL of website to collect.
    """
    _ = url
