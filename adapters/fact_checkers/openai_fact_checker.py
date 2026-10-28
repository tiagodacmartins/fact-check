import os
from dotenv import load_dotenv
from openai import OpenAI

from core.domain.article import Article
from core.domain.fact_check_result import FactCheckResult
from core.ports.fact_checker import FactCheckerPort

# Carrega as variáveis do arquivo .env
load_dotenv()

class OpenAIFactChecker(FactCheckerPort):
    def __init__(self, model: str = None):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "sua_chave_aqui":
            raise ValueError("Chave OPENAI_API_KEY não foi configurada no arquivo .env!")

        # Lê o modelo que você acabou de colocar no .env!
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=api_key)

    def check(self, article: Article, search_results: list = None) -> FactCheckResult:
        texto_limitado = article.text[:8000]

        # Formata o resumo das buscas na web para entregar à OpenAI
        contexto_busca = ""
        if search_results:
            contexto_busca = "EVIDÊNCIAS E NOTÍCIAS ENCONTRADAS NA WEB EM TEMPO REAL:\n"
            for res in search_results:
                contexto_busca += f"- Título: {res.title}\n  Fonte: {res.url}\n  Trecho: {res.snippet}\n\n"

        prompt_sistema = (
            "Você é um jornalista investigativo sênior de fact-checking. "
            "Sua missão é verificar a veracidade da matéria fornecida. "
            "IMPORTANTE: Você recebeu EVIDÊNCIAS RECENTES encontradas na web em tempo real. "
            "Cruze a matéria do usuário com essas evidências. Se outros veículos confiáveis "
            "noticiaram o mesmo fato recentemente, confirme como 'Verdadeiro'. "
            "Cite as fontes encontradas na sua justificativa."
        )

        prompt_usuario = (
            f"Matéria a ser checada:\n"
            f"Título: {article.title}\n"
            f"Autor citado: {article.author or 'Não informado'}\n"
            f"Texto:\n{texto_limitado}\n\n"
            f"{contexto_busca}"
        )

        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario},
            ],
            response_format=FactCheckResult,
        )

        return completion.choices[0].message.parsed