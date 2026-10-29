from urllib.parse import urlparse
import trafilatura
from core.domain.article import Article
from core.ports.article_extractor import ArticleExtractorPort

class TrafilaturaExtractor(ArticleExtractorPort):
    """Implementação do extrator usando a biblioteca Trafilatura"""

    def extract(self, url: str) -> Article:
        self._validate_url(url)

        # 1. Baixa o HTML da página
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            raise ConnectionError(f"Não foi possível acessar a página: {url}")

        # 2. Extrai metadados (título, autor)
        metadata = trafilatura.extract_metadata(downloaded)
        title = metadata.title if metadata and metadata.title else "Título não identificado"
        author = metadata.author if metadata else None

        # 3. Extrai apenas o corpo de texto principal (sem propagandas ou menus)
        text = trafilatura.extract(downloaded, include_comments=False)
        if not text:
            raise ValueError("Não foi possível extrair o texto principal desta página")

        return Article(url=url, title=title, text=text, author=author)

    def _validate_url(self, url: str) -> None:
        """Segurança: valida formato e evita esquemas perigosos (ex: file://, localhost)."""
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError("URL inválida. Apenas links http:// e https:// são permitidos")

        # Bloqueia acessos a rede interna local (Prevenção de SSRF)
        if parsed.hostname in ("localhost", "127.0.0.1", "0.0.0.0"):
            raise ValueError("Não é permitido analisar endereços locais.")
