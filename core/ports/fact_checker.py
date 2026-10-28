from abc import ABC, abstractmethod
from core.domain.article import Article
from core.domain.fact_check_result import FactCheckResult

class FactCheckerPort(ABC):
    """Contrato que qualquer analisador de fatos deve seguir."""

    @abstractmethod
    def check(self, article: Article) -> FactCheckResult:
        """Recebe um artigo e retorna o relatório de checagem."""
        pass