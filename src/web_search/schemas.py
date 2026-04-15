from pydantic import BaseModel, Field, HttpUrl, computed_field


class SearchResult(BaseModel):
    """Web search result."""

    url: HttpUrl
    title: str
    content: str


class SearchResults(BaseModel):
    """Normalised web search results."""

    query: str
    results: list[SearchResult] = Field(default_factory=list)

    @computed_field
    @property
    def num_results(self) -> int:
        """Number of search results."""
        return len(self.results)
