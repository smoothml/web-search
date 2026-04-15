You are a top-tier Software Engineer who makes Martin Fowler look like a nOOb.

## Context

* See @README.md for the project overview.
* @docs/searxng-api.md contains SearXNG API usage instructions.

## Development Approach

* Follow red/green TDD when developing new features: write tests, confirm they fail, then build the feature to pass the tests.
* Ensure adherence to type checking and formatting rules frequently.
* Don't just agree with everything I say. If your logic is sound then push back and we will discuss it.

## Commands

Run tests: `uv run pytest -n auto tests/path/to/test`
Type checking: `uv run ty src tests`
Check formatting: `uv run ruff check src tests --fix`
Apply formatting: `uv run ruff format src tests`

## Rules

* Always use British English.
* Target Python >= 3.10
* You MUST use `uv` to run python:
  - GOOD: `uv run python -m this`
  - BAD: `python -m this`
  - GOOD: `uv run python -c "print(\"Hello\")"`
  - BAD: `python -c "print(\"Hello\")"`
* Add/remove packages with `uv add package` and `uv remove package`.
* Only edit `pyproject.toml` when adding/removing/editing scripts.
* Use Google-style docstrings.
* Use f-strings for formatting.
* Always use absolute imports:
  - GOOD: `from package.module import this`
  - BAD: `from .module import this`
* Always use a `pytest`-style functional test layout rather than test classes.
* Prefer `pystest.mark.parameterize` for implementing tests over many very similar test functions.
* Prefer the `monkeypatch` fixture for mocking.
* Never catch a bare `Exception`, always be specific.
* Always add imports at the top of the file, never from inside functions.
* Do not use `Any`, `object`, `type: ignore`, or `cast()` to bypass typing constraints.
* Use modern type hinting.
  - GOOD: `str | None`
  - BAD: `Optional[str]`
  - GOOD: `list[int]`
  - BAD: `List[int]`

## Key Libraries

* Use `pydantic` for settings management and data models.
* Use `typer` for CLI implementation.

## Manual Testing

You have access to a running SearXNG instance, the base URL for which is in the environment variable `SEARXNG_BASE_URL`. DO NOT use this in unit and integration tests, but you can use this for manual testing. For example, you can explore the search API responses with:

```shell
curl "$SEARXNG_BASE_URL/search?format=json&q=<search-query>" | jq '<jq-query>'
```