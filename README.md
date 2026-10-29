# 🔎 Agente Autônomo de Checagem de Fatos (Fact-Checking)

Aplicação em Python que realiza checagem de fatos automatizada a partir de links de reportagens ou textos/boatos de redes sociais (WhatsApp, Instagram, X), utilizando Inteligência Artificial (OpenAI) e busca na web em tempo real (Grounding) para evitar alucinações e contornar o limite de corte de conhecimento (*knowledge cutoff*) do modelo.

---

## 🏛️ Padrão Arquitetural: Arquitetura Hexagonal (Ports & Adapters)

O projeto adota estritamente os princípios de **Clean Code** e **Arquitetura Hexagonal (Ports & Adapters)** para isolar completamente o núcleo de regras de negócio das tecnologias externas (bancos de dados, bibliotecas de scraping, provedores de IA ou interfaces de usuário).

### Diagrama Arquitetural

```
[ Adaptador CLI (CMD) ]       [ Adaptador Web (Futuro) ]
             \                         /
              v                       v
     =======================================
     CASO DE USO / CORE (Regra de Negócio)
              VerifyNewsUseCase
     =======================================
         /              |              \
        v               v               v
 [ Porta Extrator ] [ Porta Busca ] [ Porta Fact-Checker ]
        |               |               |
   (Trafilatura)      (DDGS)         (OpenAI)
```

### Estrutura de Diretórios
* **`core/domain/`**: Entidades e modelos de dados puros (`Article`, `FactCheckResult`, `SearchResult`). Não possuem dependências de frameworks externos ou bibliotecas de terceiros.
* **`core/ports/`**: Interfaces abstratas (`ABC`) definindo os contratos que conectores externos devem implementar:
  * `ArticleExtractorPort`: Contrato para baixar e extrair notícias limpas da web.
  * `SearchEnginePort`: Contrato para busca na web em tempo real.
  * `FactCheckerPort`: Contrato para envio e recebimento de análises de fatos.
* **`core/use_cases/`**: Orquestrador das regras de negócio (`VerifyNewsUseCase`). Coordena extração, busca e envio para o analisador sem conhecer detalhes de telas ou protocolos.
* **`adapters/`**: Implementações concretas das portas:
  * `extractors/`: Extração de notícias jornalísticas via biblioteca `trafilatura` com proteção contra SSRF e validação de esquemas de URL.
  * `search/`: Busca em tempo real na web usando `ddgs` (DuckDuckGo).
  * `fact_checkers/`: Integração com o SDK oficial da OpenAI com garantia de dados estruturados via Pydantic (`Structured Outputs`).
  * `cli/` (ou `main.py`): Ponto de entrada via console/terminal com menu interativo.

---

## 🔒 Boas Práticas e Segurança

* **Isolamento de Credenciais:** As chaves de API nunca são versionadas no Git. O projeto utiliza variáveis de ambiente com `python-dotenv`, mantendo `.env` no `.gitignore` e disponibilizando um modelo sem credenciais em `.env.example`.
* **Proteção contra SSRF (Server-Side Request Forgery):** O extrator de URLs valida os protocolos permitidos (`http`, `https`) e bloqueia explicitamente acessos a endereços de redes internas ou de máquina local (`localhost`, `127.0.0.1`, `0.0.0.0`).
* **Grounding e Prevenção de Alucinação:** LLMs não são tratadas como base de conhecimento estática e fechada. Toda checagem consulta fontes de notícias recentes antes de solicitar a consolidação do veredito.
* **Saídas Estruturadas (Pydantic):** A resposta da IA é forçada a obedecer ao esquema do modelo `FactCheckResult`, garantindo tipos consistentes (`verdict`, `confidence_score`, `summary`, `key_claims`, `sources_consulted`).

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
* Python 3.10 ou superior
* Chave de API da OpenAI

### 2. Passo a Passo

1. **Clone o repositório e crie o ambiente virtual:**
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd checagem
   python -m venv venv
   ```

2. **Ative o ambiente virtual:**
   * **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * **Windows (CMD):**
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   * **Linux / macOS:**
     ```bash
     source venv/bin/activate
     ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   * Crie o arquivo `.env` na raiz do projeto baseado no `.env.example`:
     ```text
     OPENAI_API_KEY=sua_chave_openai_aqui
     OPENAI_MODEL=gpt-4o-mini
     ```

5. **Inicie o programa:**
   ```bash
   python main.py
   ```

---

## 🗺️ Próximos Passos (Roadmap)

- [x] Extração limpa de artigos de notícias jornalísticas
- [x] Integração com OpenAI usando Structured Outputs
- [x] Grounding com busca web em tempo real (DuckDuckGo)
- [x] Checagem de boatos em texto direto (WhatsApp / Instagram / X)
- [x] Interface CLI interativa em terminal
- [ ] Interface gráfica Web (Streamlit ou FastAPI)
- [ ] Testes automatizados unitários com mocks

