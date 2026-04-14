# SearXNG Search API: implementation notes

## Use this mental model

SearXNG exposes a search HTTP API over one or more upstream search engines.

For a client using an already configured instance:
- send a query with `q`
- request JSON with `format=json`
- optionally constrain engines, language, pagination, and recency
- expect some behaviour to vary by engine, especially query syntax and filters

Assume the endpoint is already operational and JSON responses are available.

## Endpoints

Equivalent search endpoints:
- `GET /search`
- `POST /search`

Use `GET` for simple requests and debugging.
Use `POST` with form data when the query becomes long or awkward to encode in the URL.

## Required input

### `q`
The only required parameter.

`q` is the search query string. It is passed through to the underlying search engines, so operators such as `site:`, exact quotes, and other advanced syntax are engine-dependent. A query can behave differently depending on which engines are active.

## Preferred response format

### `format=json`
Use JSON for programmatic clients.

Documented formats include:
- `json`
- `csv`
- `rss`

For programmatic use, assume `json` and ignore the others unless explicitly needed.

## Parameters that matter operationally

### Engine and category control
- `categories`: comma-separated categories
- `engines`: comma-separated engines
- `enabled_engines`: engines to enable
- `disabled_engines`: engines to disable

Implementation rule: pick one control style and use it consistently. In most clients, `engines` is the clearest.

Example:

```http
GET /search?q=vector+database&format=json&engines=google,duckduckgo
```

### Pagination

`pageno`: page number, defaults to `1`. Example:

```http
GET /search?q=vector+database&format=json&pageno=2
```

### Recency

`time_range`: `day`, `month`, or `year`. This is best-effort. It only has effect on engines that support recency filtering. Example:

```http
GET /search?q=browser+security&format=json&time_range=month
```

### Language

`language`: language code. Use this when language drift matters. Example:

```http
GET /search?q=privacy+law&format=json&language=en-GB
```

### Safe search

`safesearch`: `0`, `1`, or `2`. This is also best-effort and depends on engine support. Example:

```http
GET /search?q=image+search&format=json&safesearch=2
```

## Parameters usually irrelevant to backend agents

These are primarily UI-facing or browser-facing and usually do not matter in a backend integration:

* `results_on_new_tab`
* `image_proxy`
* `autocomplete`
* `theme`
* `enabled_plugins`
* `disabled_plugins`

Ignore them unless you have a specific reason to control them.

## Failure and variance model

A client should assume the transport is stable but the search semantics are only partly standardised.

### 1. Query semantics vary by engine

Advanced operators inside `q` are not guaranteed to behave uniformly. `site:github.com foo` may work well with one engine and degrade with another.

### 2. Filters are best-effort

`time_range` and `safesearch` only work where the selected engines support them.

### 3. Results are not deterministic

Changing engines, language, or page number can materially alter results. Even with the same request, upstream engines may return changing rankings over time.

## Client strategy

### Baseline request

Use:

```http
GET /search?q=<query>&format=json
```

or:

```http
POST /search
Content-Type: application/x-www-form-urlencoded

q=<query>&format=json
```

### Determinism strategy

If reproducibility matters:

* pin `engines`
* pin `language`
* send `pageno` explicitly
* avoid relying on advanced query operators unless they are known to work with the chosen engines

### Good defaults

Use:

* `format=json`
* explicit `engines` when consistency matters
* explicit `language` when localisation matters
* explicit `pageno=1` even though it is the default

Avoid:

* UI-only parameters unless required
* assuming all engines interpret `q` the same way
* assuming recency and safe-search filters are uniformly enforced

## Minimal examples

### Simple JSON search

```bash
curl '<base-url>/search?q=searxng&format=json'
```

### POST search

```bash
curl -X POST '<base-url>/search' \
  -d 'q=searxng' \
  -d 'format=json'
```

### Engine-pinned search

```bash
curl '<base-url>/search?q=site:github.com+searxng&format=json&engines=google,duckduckgo'
```

### Recency-filtered search

```bash
curl '<base-url>/search?q=privacy+search&format=json&time_range=month'
```

### Language-pinned search

```bash
curl '<base-url>/search?q=cybersecurity+policy&format=json&language=en-GB'
```

## Bottom line for the agent

Treat SearXNG as a search API with a stable HTTP interface but partially engine-dependent semantics.

The practical contract is:

* send `q`
* request `format=json`
* optionally pin engines, language, page, and recency
* expect some query features and filters to vary by engine