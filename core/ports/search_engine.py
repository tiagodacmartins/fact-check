from abc import ABC, abstractmethod
from typing import List
from core.domain.search_result import SearchResult

class SearchEnginePort(ABC):
    """Contrato para mecanismos de busca na web."""

    @abstractmethod
    def search(self, query: str, max_results: int = 4) -> List[SearchResult]:
        """Faz uma busca na internet e retorna uma lista de resultados."""
        pass