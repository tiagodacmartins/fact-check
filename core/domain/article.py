from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Article:
    """Representa um artigo ou notícia extraído da web."""
    url: str
    title: str
    text: str
    author: Optional[str] = None

    def __post_init__(self):
        # Valida se um artigo não tem o texto vazio
        if not self.text or not self.text.strip():
            raise ValueError("O texto do artigo não pode ser vazio.")
        