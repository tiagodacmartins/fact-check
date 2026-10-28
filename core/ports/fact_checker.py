from abc import ABC, abstractmethod
from typing import Optional, List
from core.domain.article import Article
from core.domain.fact_check_result import FactCheckResult

class FactCheckerPort(ABC):
    """Contrato que qualquer analisador de fatos deve seguir."""

    @abstractmethod
    def check(self, article: Article, search_results: Optional[List] = None) -> FactCheckResult:
        """Recebe um artigo e evidências da web e retorna o relatório de checagem."""
        pass