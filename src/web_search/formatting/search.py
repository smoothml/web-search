from web_search.schemas import SearchResults


def render_search_results_markdown(search_results: SearchResults) -> str:
    """Render search results as markdown for CLI output.

    Args:
        search_results: Structured search result payload.

    Returns:
        The rendered markdown output.
    """
    lines = [
        "# Search results",
        "",
        f"Search query: {search_results.query}",
        f"Number of results: {search_results.num_results}",
        "",
    ]

    if search_results.num_results == 0:
        lines.append("No results found.")
    else:
        for index, result in enumerate(search_results.results, start=1):
            lines.append(f"{index}. [{result.title}]({str(result.url)})")
            lines.append(f"   {result.content}")
            lines.append("")

    return "\n".join(lines).rstrip()
