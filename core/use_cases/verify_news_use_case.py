from core.ports.article_extractor import ArticleExtractorPort
from core.ports.fact_checker import FactCheckerPort
from core.ports.search_engine import SearchEnginePort
from core.domain.fact_check_result import FactCheckResult
from core.domain.article import Article

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

    def execute_from_url(self, url: str) -> FactCheckResult:
        """Checagem a partir de um link da web."""
        # 1. Extrai o artigo
        article = self.extractor.extract(url)

        # 2. Busca na web sobre o título da notícia
        print(f"-> Pesquisando notícias recentes sobre: '{article.title}'...")
        search_results = self.search_engine.search(article.title, max_results=4)

        # 3. Envia para a OpenAI
        print("-> Cruzando informações com a OpenAI...")
        return self.fact_checker.check(article, search_results=search_results)

    def execute_from_text(self, claim_text: str) -> FactCheckResult:
        """Checagem a partir de um texto/boato direto (WhatsApp/Instagram/X)."""
        # 1. Empacota o texto dentro de um Article (sem precisar raspar a web)
        article = Article(
            url="entrada-manual",
            title="Alegação enviada diretamente pelo usuário",
            text=claim_text,
            author="Não informado"
        )

        # 2. Usa o próprio texto do boato para pesquisar no DuckDuckGo (limitado a 100 caracteres na busca)
        termo_busca = claim_text[:100].strip()
        print(f"-> Pesquisando na web por evidências sobre: '{termo_busca}'...")
        search_results = self.search_engine.search(termo_busca, max_results=4)

        # 3. Envia para a OpenAI
        print("-> Cruzando informações com a OpenAI...")
        return self.fact_checker.check(article, search_results=search_results)