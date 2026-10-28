from adapters.extractors.trafilatura_extractor import TrafilaturaExtractor
from adapters.search.duckduckgo_search_adapter import DuckDuckGoSearchAdapter
from adapters.fact_checkers.openai_fact_checker import OpenAIFactChecker
from core.use_cases.verify_news_use_case import VerifyNewsUseCase

def main():
    # Montamos os blocos de lego (Injeção de Dependências):
    use_case = VerifyNewsUseCase(
        extractor=TrafilaturaExtractor(),
        search_engine=DuckDuckGoSearchAdapter(),
        fact_checker=OpenAIFactChecker()
    )

    url = input("Digite ou cole o link da reportagem: ").strip()
    if not url:
        return

    try:
        print("\n🔎 Iniciando investigação...")
        result = use_case.execute(url)

        print("\n" + "=" * 50)
        print("📋 RELATÓRIO DE CHECAGEM DE FATOS (COM BUSCA EM TEMPO REAL)")
        print("=" * 50)
        print(f"🎯 Veredito: {result.verdict.upper()}")
        print(f"📊 Nível de Confiança: {result.confidence_score}%")
        print(f"\n📝 Resumo da Análise:\n{result.summary}")
        
        print("\n🔍 Principais alegações analisadas:")
        for claim in result.key_claims:
            print(f"  • {claim}")

        if result.sources_consulted:
            print("\n🌐 Fontes e referências identificadas:")
            for source in result.sources_consulted:
                print(f"  🔗 {source}")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    main()