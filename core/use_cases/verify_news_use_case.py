from core.ports.article_extractor import ArticleExtractorPort
from core.ports.fact_checker import FactCheckerPort
from core.ports.search_engine import SearchEnginePort
from core.domain.fact_check_result import FactCheckResult

class VerifyNewsUseCase:
    """Caso de uso que orquestra todo o fluxo de checagem."""

    def __init__(
        self,
        extractor: ArticleExtractorPort,
        search_engine: SearchEnginePort,
        fact_checker: FactCheckerPort,
    ):
        self.extractor = extractor
        self.search_engine = search_engine
        self.fact_checker = fact_checker

    def execute(self, url: str) -> FactCheckResult:
        # 1. Extrai o artigo
        article = self.extractor.extract(url)

        # 2. Busca na web sobre o título do artigo para checar o que outros jornais dizem
        print(f"-> Pesquisando notícias recentes na internet sobre: '{article.title}'...")
        search_results = self.search_engine.search(article.title, max_results=4)

        # 3. Envia o artigo + o que encontrou na web para a OpenAI
        print("-> Cruzando informações com a OpenAI...")
        result = self.fact_checker.check(article, search_results=search_results)

        return result