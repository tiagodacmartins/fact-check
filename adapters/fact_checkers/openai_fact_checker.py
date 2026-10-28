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

    def check(self, article: Article) -> FactCheckResult:
        # Limita para não gastar créditos excessivos se o texto for gigante
        texto_limitado = article.text[:10000]

        prompt_sistema = (
            "Você é um jornalista investigativo sênior e especialista em checagem de fatos (fact-checking). "
            "Sua tarefa é analisar criticamente o texto fornecido. "
            "Identifique sensacionalismo, alegações extraordinárias sem comprovação e coerência das informações. "
            "Se o assunto exigir dados posteriores ao seu conhecimento ou faltarem evidências, classifique como 'Inconclusivo'."
        )

        prompt_usuario = (
            f"Título da Matéria: {article.title}\n"
            f"Autor citado: {article.author or 'Não informado'}\n"
            f"Conteúdo:\n{texto_limitado}"
        )

        # Chama a OpenAI forçando a resposta vir preenchida no modelo FactCheckResult
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario},
            ],
            response_format=FactCheckResult,
        )

        return completion.choices[0].message.parsed