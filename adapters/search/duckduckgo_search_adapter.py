from typing import List
from duckduckgo_search import DDGS
from core.domain.search_result import SearchResult
from core.ports.search_engine import SearchEnginePort

class DuckDuckGoSearchAdapter(SearchEnginePort):
    """Adaptador de busca gratuito usando DuckDuckGo."""

    def search(self, query: str, max_results: int = 4) -> List[SearchResult]:
        results: List[SearchResult] = []
        
        try:
            # Usa o DuckDuckGo para buscar textos em tempo real
            with DDGS() as ddgs:
                search_data = ddgs.text(query, max_results=max_results)
                
                if search_data:
                    for item in search_data:
                        results.append(
                            SearchResult(
                                title=item.get("title", ""),
                                url=item.get("href", ""),
                                snippet=item.get("body", "")
                            )
                        )
        except Exception as e:
            # Se a busca falhar por instabilidade, não quebramos o app inteiro
            print(f"[Aviso] Falha ao consultar busca na web: {e}")

        return results