import html
import streamlit as st
from adapters.extractors.trafilatura_extractor import TrafilaturaExtractor
from adapters.search.duckduckgo_search_adapter import DuckDuckGoSearchAdapter
from adapters.fact_checkers.openai_fact_checker import OpenAIFactChecker
from core.use_cases.verify_news_use_case import VerifyNewsUseCase

# 1. Configuração da página
st.set_page_config(
    page_title="Windows PowerShell - Checador de Fatos",
    page_icon="💻",
    layout="wide"
)

# 2. CSS Estilo Windows PowerShell Autêntico
st.markdown("""
<style>
    /* Fundo clássico do Windows PowerShell (#012456) */
    .stApp, header[data-testid="stHeader"] {
        background-color: #012456 !important;
        color: #EEEDF0 !important;
        font-family: 'Consolas', 'Cascadia Mono', 'Courier New', monospace !important;
    }

    /* Esconde elementos visuais web desnecessários do Streamlit */
    #MainMenu, footer, [data-testid="stToolbar"] {
        visibility: hidden !important;
    }

    /* Ajusta o espaçamento do topo para parecer uma janela de console real */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1150px !important;
    }

    /* Remove arredondamentos e força fonte monoespaçada em todos os elementos */
    * {
        font-family: 'Consolas', 'Cascadia Mono', 'Courier New', monospace !important;
        border-radius: 0px !important;
    }

    h1, h2, h3, p, span, label, div {
        color: #EEEDF0;
    }

    /* Banner ASCII Art */
    .ps-ascii {
        color: #00FFFF !important;
        font-family: 'Consolas', 'Cascadia Mono', 'Courier New', monospace !important;
        font-size: 13px !important;
        line-height: 1.15 !important;
        background-color: transparent !important;
        padding: 8px 0px !important;
        margin: 6px 0px !important;
        overflow-x: auto !important;
        white-space: nowrap !important;
    }

    /* Estilização do Seletor de Modo (st.radio horizontal tipo switches de CLI) */
    div[role="radiogroup"] {
        background-color: #001737 !important;
        border: 1px solid #4A6B9C !important;
        padding: 8px 14px !important;
        gap: 24px !important;
    }

    div[role="radiogroup"] label {
        color: #FFFFFF !important;
        font-weight: bold !important;
        cursor: pointer !important;
    }

    /* Containers de Input e TextArea (BaseWeb do Streamlit) */
    [data-baseweb="input"],
    [data-baseweb="textarea"],
    [data-baseweb="base-input"] {
        background-color: #00122B !important;
        border: 1px solid #4A6B9C !important;
    }

    /* Campos de digitação (Input e TextArea) */
    .stTextInput input,
    .stTextArea textarea {
        background-color: #00122B !important;
        color: #00FFFF !important;
        caret-color: #FFFF00 !important;
        font-family: 'Consolas', 'Cascadia Mono', monospace !important;
        font-size: 15px !important;
        -webkit-text-fill-color: #00FFFF !important;
        padding: 10px !important;
    }

    /* Cor do Placeholder */
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #5C7DA8 !important;
        -webkit-text-fill-color: #5C7DA8 !important;
        opacity: 1 !important;
    }

    /* Foco nos campos */
    [data-baseweb="input"]:focus-within,
    [data-baseweb="textarea"]:focus-within {
        border-color: #FFFF00 !important;
        box-shadow: 0 0 0 1px #FFFF00 !important;
    }

    /* Botão estilo comando PowerShell */
    .stButton > button {
        background-color: #001737 !important;
        color: #FFFF00 !important;
        border: 1px solid #FFFF00 !important;
        font-weight: bold !important;
        font-size: 14px !important;
        padding: 6px 20px !important;
        transition: none !important;
    }

    .stButton > button:hover {
        background-color: #FFFF00 !important;
        color: #012456 !important;
    }

    .stButton > button:hover * {
        color: #012456 !important;
    }

    /* Bloco de saída tipo console */
    .ps-output-box {
        background-color: #00122B;
        border: 1px solid #4A6B9C;
        padding: 16px;
        margin-top: 14px;
        font-family: 'Consolas', monospace;
        line-height: 1.5;
    }

    /* Bloco de erro nativo do PowerShell (Write-Error) */
    .ps-error-box {
        background-color: #001024;
        border-left: 3px solid #FF5555;
        padding: 10px 14px;
        margin-top: 12px;
        color: #FF5555 !important;
        font-family: 'Consolas', monospace;
        white-space: pre-wrap;
    }

    /* Cores de Sintaxe PSReadLine (PowerShell 5.1 / 7) */
    .ps-prompt { color: #EEEDF0 !important; }
    .ps-cmdlet { color: #FFFF00 !important; font-weight: bold; }
    .ps-param  { color: #A8B5C2 !important; }
    .ps-string { color: #00FFFF !important; }
    .ps-comment { color: #57A64A !important; }
    .ps-green  { color: #00FF66 !important; font-weight: bold; }
    .ps-red    { color: #FF5555 !important; font-weight: bold; }
    .ps-yellow { color: #FFFF00 !important; font-weight: bold; }
    .ps-muted  { color: #8A9BA8 !important; }
</style>
""", unsafe_allow_html=True)

# 3. Inicializa o Caso de Uso
@st.cache_resource
def get_use_case():
    return VerifyNewsUseCase(
        extractor=TrafilaturaExtractor(),
        search_engine=DuckDuckGoSearchAdapter(),
        fact_checker=OpenAIFactChecker()
    )

use_case = get_use_case()

def render_ps_error(cmd_name: str, message: str):
    safe_msg = html.escape(message)
    st.markdown(
        f"""<div class="ps-error-box">{cmd_name} : {safe_msg}
No linha:1 caractere:1
+ {cmd_name}
+ ~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [{cmd_name}], RuntimeException
    + FullyQualifiedErrorId : FactCheckExecutionError</div>""",
        unsafe_allow_html=True
    )

# 4. Cabeçalho Clássico do Windows PowerShell + Banner ASCII "CHECADOR DE FATOS"
ascii_lines = [
    r"  ____  _   _  _____   ____     _     ____    ___   ____      ____   _____     _____     _     _____   ___   ____  ",
    r" / ___|| | | || ____| / ___|   / \   |  _ \  / _ \ |  _ \    |  _ \ | ____|   |  ___|   / \   |_   _| / _ \ / ___| ",
    r"| |    | |_| ||  _|  | |      / _ \  | | | || | | || |_) |   | | | ||  _|     | |_     / _ \    | |  | | | |\___ \ ",
    r"| |___ |  _  || |___ | |___  / ___ \ | |_| || |_| ||  _ <    | |_| || |___    |  _|   / ___ \   | |  | |_| | ___) |",
    r" \____||_| |_||_____| \____|/_/   \_\|____/  \___/ |_| \_\   |____/ |_____|   |_|    /_/   \_\  |_|   \___/ |____/ ",
]
ascii_html = "<br/>".join(html.escape(line).replace(" ", "&nbsp;") for line in ascii_lines)

st.markdown(f"""
<div>
    Windows PowerShell<br/>
    Copyright (C) Tiaguedesoft Corporation. Todos os direitos reservados.<br/><br/>
    <span class="ps-prompt">PS C:\\Users\\Admin\\FactCheck&gt;</span> <span class="ps-cmdlet">Import-Module</span> <span class="ps-string">.\\ChecadorDeFatos.psd1</span>
</div>
<div class="ps-ascii">{ascii_html}</div>
<div style="border-bottom: 1px solid #4A6B9C; padding-bottom: 10px; margin-bottom: 16px;">
    <span class="ps-comment"># Módulo carregado com sucesso. Selecione o parâmetro de entrada abaixo (-Url ou -Text).</span>
</div>
""", unsafe_allow_html=True)

# 5. Seletor de Parâmetro estilo PowerShell Switch
st.markdown(
    "<span class='ps-prompt'>PS C:\\Users\\Admin\\FactCheck&gt;</span> "
    "<span class='ps-cmdlet'>Set-ExecutionMode</span> <span class='ps-param'>-ParameterSetName</span>",
    unsafe_allow_html=True
)

modo = st.radio(
    "Modo de execução:",
    ["-Url (Link de Reportagem / Notícia)", "-Text (Declaração ou Boato de Rede Social)"],
    horizontal=True,
    label_visibility="collapsed",
    key="modo_selecao"
)

st.markdown("<br/>", unsafe_allow_html=True)

# 6. Entrada de Dados e Execução
if "-Url" in modo:
    st.markdown(
        "<span class='ps-prompt'>PS C:\\Users\\Admin\\FactCheck&gt;</span> "
        "<span class='ps-cmdlet'>Invoke-FactCheck</span> <span class='ps-param'>-Url</span>",
        unsafe_allow_html=True
    )
    url_input = st.text_input(
        "URL:",
        placeholder="https://g1.globo.com/...",
        label_visibility="collapsed",
        key="input_url"
    )
    executar = st.button("[ Enter ] Executar Comando", key="btn_run_url")

    if executar:
        if not url_input.strip():
            render_ps_error("Invoke-FactCheck -Url", "Não é possível associar o argumento ao parâmetro 'Url' porque ele é uma cadeia de caracteres vazia.")
        else:
            with st.spinner("VERBOSE: [Trafilatura] Baixando conteúdo da URL e [DDGS] consultando fontes em tempo real..."):
                try:
                    st.session_state["resultado"] = use_case.execute_from_url(url_input)
                    st.session_state["ultimo_comando"] = f'Invoke-FactCheck -Url "{url_input}"'
                except Exception as e:
                    render_ps_error("Invoke-FactCheck -Url", str(e))

else:
    st.markdown(
        "<span class='ps-prompt'>PS C:\\Users\\Admin\\FactCheck&gt;</span> "
        "<span class='ps-cmdlet'>Invoke-FactCheck</span> <span class='ps-param'>-Text</span>",
        unsafe_allow_html=True
    )
    texto_input = st.text_area(
        "Texto:",
        placeholder="Cole ou digite aqui o texto da notícia, corrente de WhatsApp ou postagem do X/Instagram...",
        label_visibility="collapsed",
        height=120,
        key="input_texto"
    )
    executar = st.button("[ Enter ] Executar Comando", key="btn_run_text")

    if executar:
        if not texto_input.strip():
            render_ps_error("Invoke-FactCheck -Text", "Não é possível associar o argumento ao parâmetro 'Text' porque ele é uma cadeia de caracteres vazia.")
        else:
            with st.spinner("VERBOSE: [DDGS] Buscando evidências recentes na web e [OpenAI] analisando veracidade..."):
                try:
                    st.session_state["resultado"] = use_case.execute_from_text(texto_input)
                    trecho = texto_input[:60].replace("\n", " ") + ("..." if len(texto_input) > 60 else "")
                    st.session_state["ultimo_comando"] = f'Invoke-FactCheck -Text "{trecho}"'
                except Exception as e:
                    render_ps_error("Invoke-FactCheck -Text", str(e))

# 7. Exibição do Relatório em formato Format-List / Format-Table do PowerShell
if "resultado" in st.session_state:
    res = st.session_state["resultado"]
    v_upper = res.verdict.upper()

    cor_classe = "ps-yellow"
    if "VERDADEIRO" in v_upper:
        cor_classe = "ps-green"
    elif "FALSO" in v_upper:
        cor_classe = "ps-red"

    resumo_seguro = html.escape(res.summary)

    st.markdown(f"""
    <div class="ps-output-box">
        <span class="ps-prompt">PS C:\\Users\\Admin\\FactCheck&gt;</span> <span class="ps-cmdlet">Get-FactCheckResult</span> <span class="ps-param">|</span> <span class="ps-cmdlet">Format-List</span><br/><br/>
        <table style="width: 100%; border-collapse: collapse; border: none;">
            <tr>
                <td style="padding: 4px 8px 4px 0px; color: #00FFFF; width: 170px; vertical-align: top;">Verdict</td>
                <td style="padding: 4px 8px; color: #EEEDF0; width: 15px; vertical-align: top;">:</td>
                <td style="padding: 4px 0px;"><span class="{cor_classe}">[{v_upper}]</span></td>
            </tr>
            <tr>
                <td style="padding: 4px 8px 4px 0px; color: #00FFFF; vertical-align: top;">ConfidenceScore</td>
                <td style="padding: 4px 8px; color: #EEEDF0; vertical-align: top;">:</td>
                <td style="padding: 4px 0px; color: #FFFFFF;">{res.confidence_score}%</td>
            </tr>
            <tr>
                <td style="padding: 4px 8px 4px 0px; color: #00FFFF; vertical-align: top;">Summary</td>
                <td style="padding: 4px 8px; color: #EEEDF0; vertical-align: top;">:</td>
                <td style="padding: 4px 0px; color: #EEEDF0;">{resumo_seguro}</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br/><span class='ps-prompt'>PS C:\\Users\\Admin\\FactCheck&gt;</span> <span class='ps-cmdlet'>Get-ExaminedClaims</span>", unsafe_allow_html=True)
    for i, claim in enumerate(res.key_claims, 1):
        st.markdown(f"<span style='color: #A0B0C0;'>[{i}]</span> {html.escape(claim)}", unsafe_allow_html=True)

    if res.sources_consulted:
        st.markdown("<br/><span class='ps-prompt'>PS C:\\Users\\Admin\\FactCheck&gt;</span> <span class='ps-cmdlet'>Get-ConsultedSources</span>", unsafe_allow_html=True)
        for source in res.sources_consulted:
            source_seguro = html.escape(source)
            if source.startswith("http"):
                st.markdown(f"- <a href='{source_seguro}' target='_blank' style='color: #00FFFF; text-decoration: underline;'>{source_seguro}</a>", unsafe_allow_html=True)
            else:
                st.markdown(f"- <span style='color: #F1F1F1;'>{source_seguro}</span>", unsafe_allow_html=True)
