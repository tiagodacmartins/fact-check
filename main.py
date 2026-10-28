from adapters.extractors.trafilatura_extractor import TrafilaturaExtractor

def main():
    extractor = TrafilaturaExtractor()
    
    # Coloque aqui o link de uma notícia real qualquer (ex: G1, BBC, Folha, etc.)
    url_teste = "https://www.ea.com/pt-br/games/battlefield/battlefield-6/news/battlefield-6-game-update-2-1-1-0" 

    print(f"Buscando notícia: {url_teste}...")
    try:
        article = extractor.extract(url_teste)
        print("\n=== SUCESSO! ===")
        print(f"Título: {article.title}")
        print(f"Autor: {article.author}")
        print(f"Tamanho do texto: {len(article.text)} caracteres")
        print("\nTrecho inicial:")
        print(article.text[:1000] + "...")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()