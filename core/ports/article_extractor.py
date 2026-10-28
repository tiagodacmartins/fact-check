from abc import ABC, abstractmethod
from core.domain.article import Article

class ArticleExtractorPort(ABC):
    """Contrato que qualquer extrator de notícia deve seguir"""

    @abstractmethod
    def extract(self, url: str) -> Article:
        """Extrai o título e o texto de uma URL e retorna um Article"""
        pass