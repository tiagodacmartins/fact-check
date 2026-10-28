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
        description="Um resumo claro explicando o veredito com base nas notícias e fontes cruzadas."
    )
    key_claims: List[str] = Field(
        description="Lista com as 2 a 4 principais afirmações feitas no texto."
    )
    sources_consulted: List[str] = Field(
        default_factory=list,
        description="Links ou nomes dos veículos de imprensa encontrados que confirmam ou desmentem o fato."
    )