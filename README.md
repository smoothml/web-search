# Web Search

`web-seach` is a CLI tool backed by [SearXNG](https://docs.searxng.org/) enabling developers and agents to search the web and extract site content.

## Project Overview

### Project Structure

```
.
├── docs                 # Documentation to aid your development process
├── src
│   └── web_search
│       ├── libs         # Libraries for interfacing with external tools and services
│       ├── services     # Orchestration layer
│       ├── cli.py       # Typer CLI
│       ├── constants.py # Application-wide constants
│       ├── enums.py     # Application-wide enums
│       └── schemas.py   # Pydantic data models
├── tests
├── AGENTS.md
├── pyproject.toml
├── README.md
└── uv.lock
```