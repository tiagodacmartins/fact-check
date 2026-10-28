from pydantic import BaseModel, Field
from typing import List

class FactCheckResult(BaseModel):
    """Representa a resposta estruturada da checagem de fatos."""
    verdict: str = Field(
        description="O veredito final: 'Verdadeiro', 'Falso', 'Enganoso' ou 'Inconclusivo'."
    )
    confidence_score: int = Field(
        description="Nível de certeza da análise, de 0 a 100."
    )
    summary: str = Field(
        description="Um resumo claro e objetivo em 2 a 3 frases explicando o motivo do veredito."
    )
    key_claims: List[str] = Field(
        description="Lista com as 2 a 4 principais afirmações feitas no texto que foram analisadas."
    )