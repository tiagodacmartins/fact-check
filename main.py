from adapters.extractors.trafilatura_extractor import TrafilaturaExtractor
from adapters.fact_checkers.openai_fact_checker import OpenAIFactChecker

def main():
    # 1. Instancia as nossas ferramentas
    extractor = TrafilaturaExtractor()
    checker = OpenAIFactChecker()

    # 2. Pede um link para o usuário no terminal
    url = input("Digite ou cole o link da reportagem: ").strip()

    if not url:
        print("URL não pode ser vazia!")
        return

    try:
        print("\n[1/2] 📥 Acessando a página e extraindo o texto...")
        article = extractor.extract(url)
        print(f"-> Notícia encontrada: '{article.title}'")

        print(f"\n[2/2] 🤖 Analisando com OpenAI ({checker.model})... Aguarde alguns segundos...")
        result = checker.check(article)

        # 3. Exibe o relatório final de forma organizada
        print("\n" + "=" * 50)
        print("📋 RELATÓRIO DE CHECAGEM DE FATOS")
        print("=" * 50)
        print(f"🎯 Veredito: {result.verdict.upper()}")
        print(f"📊 Nível de Confiança: {result.confidence_score}%")
        print(f"\n📝 Resumo da Análise:\n{result.summary}")
        
        print("\n🔍 Principais alegações analisadas:")
        for claim in result.key_claims:
            print(f"  • {claim}")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()