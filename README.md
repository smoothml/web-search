# Web Search

`web-seach` is a CLI tool backed by [SearXNG](https://docs.searxng.org/) enabling developers and agents to search the web and extract site content.

## Usage

You require access to a [SearXNG](https://docs.searxng.org/) instance with JSON search responses enabled. Set the `SEARXNG_BASE_URL` environment variable to the instance base URL.

Install the CLI globally:

```
uv tool install git+https://github.com/smoothml/web-search
```

Usage:

```
# Search the web
web search <search-query>

# Specify the number of results to return (defaults to 10)
web search <search-query> --num-results 3

# Return a JSON object instead of markdown formatted text
web search <search-query> --json
```

## Local Development

```
# Install dependencies
uv sync

# Run tests
uv run pytest -n auto tests/path/to/test

# Type checking
uv run ty src tests

# Check formatting
uv run ruff check src tests --fix

# Apply formatting
uv run ruff format src tests
```

### Project Structure

```
.
├── docs                 # Documentation to aid development
├── src
│   └── web_search
│       ├── formatting   # Tools for response formatting
│       ├── libs         # Libraries for interfacing with external tools and services
│       │   └── searxng  # SearXNG interface
│       ├── services     # Orchestration layer
│       │   └── search   # Web search service
│       ├── cli.py       # Typer CLI
│       ├── constants.py # Application-wide constants
│       ├── enums.py     # Application-wide enums
│       ├── schemas.py   # Pydantic data models
│       └── settings.py  # Application settings
├── tests                # Application tests with a structure mirroring src
├── AGENTS.md
├── pyproject.toml
├── README.md
└── uv.lock
```