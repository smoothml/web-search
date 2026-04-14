import typer

app = typer.Typer(help="Web search CLI.")


@app.command()
def search(query: str) -> str:
    """Run a web search.

    Args:
        query: Search query string.

    Returns:
        The search result.
    """
    return ""


@app.command()
def get_content(url: str) -> str:
    """Get website content converted to markdown format (best effort).

    Args:
        url: URL of website to collect.

    Returns:
        The website content in markdown format.
    """
    return ""
