from adapters.extractors.trafilatura_extractor import TrafilaturaExtractor
from adapters.search.duckduckgo_search_adapter import DuckDuckGoSearchAdapter
from adapters.fact_checkers.openai_fact_checker import OpenAIFactChecker
from core.use_cases.verify_news_use_case import VerifyNewsUseCase
from core.domain.fact_check_result import FactCheckResult

def exibir_relatorio(result: FactCheckResult):
    print("\n" + "=" * 55)
    print("📋 RELATÓRIO DE CHECAGEM DE FATOS")
    print("=" * 55)
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
    print("=" * 55 + "\n")

def main():
    use_case = VerifyNewsUseCase(
        extractor=TrafilaturaExtractor(),
        search_engine=DuckDuckGoSearchAdapter(),
        fact_checker=OpenAIFactChecker()
    )

    while True:
        print("========================================")
        print("🔎 AGENTE DE CHECAGEM DE FATOS")
        print("========================================")
        print("[1] Checar link de reportagem / notícia")
        print("[2] Checar texto de boato")
        print("[0] Sair do programa")
        
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "0":
            print("Até logo!")
            break
        elif opcao == "1":
            url = input("\nCole o link da reportagem: ").strip()
            if not url:
                continue
            try:
                print("\nIniciando investigação por link...")
                result = use_case.execute_from_url(url)
                exibir_relatorio(result)
            except Exception as e:
                print(f"\n❌ Erro: {e}\n")
        elif opcao == "2":
            texto = input("\nCole ou digite o texto do boato: ").strip()
            if not texto:
                continue
            try:
                print("\nIniciando investigação pelo texto...")
                result = use_case.execute_from_text(texto)
                exibir_relatorio(result)
            except Exception as e:
                print(f"\n❌ Erro: {e}\n")
        else:
            print("\n⚠️ Opção inválida! Tente novamente.\n")

if __name__ == "__main__":
    main()