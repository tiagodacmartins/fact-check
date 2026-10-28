from dataclasses import dataclass

@dataclass(frozen=True)
class SearchResult:
    """Representa um resultado encontrado na busca da web."""
    title: str
    url: str
    snippet: str  # É o trecho de texto que aparece embaixo do link no buscador