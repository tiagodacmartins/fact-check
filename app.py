import streamlit as st
from adapters.extractors.trafilatura_extractor import TrafilaturaExtractor
from adapters.search.duckduckgo_search_adapter import DuckDuckGoSearchAdapter
from adapters.fact_checkers.openai_fact_checker import OpenAIFactChecker
from core.use_cases.verify_news_use_case import VerifyNewsUseCase

# 1. Configuração da página
st.set_page_config(
    page_title="Windows PowerShell - FactCheck",
    page_icon="💻",
    layout="wide"
)

# 2. CSS Estilo PowerShell Real (Azul clássico, fonte Consolas, bordas retas)
st.markdown("""
<style>
    /* PowerShell Classic Blue Theme */
    .stApp {
        background-color: #012456 !important;
        color: #F1F1F1 !important;
        font-family: 'Consolas', 'Cascadia Code', 'Courier New', monospace !important;
    }

    /* Remove arredondamentos e aplica fonte monospace em tudo */
    * {
        font-family: 'Consolas', 'Cascadia Code', 'Courier New', monospace !important;
        border-radius: 0px !important;
    }

    /* Textos e Labels */
    h1, h2, h3, p, span, label, div {
        color: #F1F1F1 !important;
    }

    /* Caixas de Texto estilo Prompt do PowerShell */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {
        background-color: #001737 !important;
        color: #FFFFFF !important;
        border: 1px solid #7F9FBF !important;
        font-family: 'Consolas', monospace !important;
        font-size: 14px !important;
    }

    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus {
        border-color: #FFFFFF !important;
        box-shadow: none !important;
    }

    /* Botão estilo terminal */
    .stButton > button {
        background-color: #001737 !important;
        color: #FFFF00 !important;
        border: 1px solid #FFFF00 !important;
        font-weight: bold !important;
        font-size: 14px !important;
        padding: 6px 18px !important;
    }

    .stButton > button:hover {
        background-color: #FFFF00 !important;
        color: #012456 !important;
    }

    /* Bloco de saída tipo console */
    .ps-output-box {
        background-color: #001737;
        border: 1px solid #7F9FBF;
        padding: 16px;
        margin-top: 15px;
        font-family: 'Consolas', monospace;
    }

    .ps-prompt { color: #FFFF00; font-weight: bold; }
    .ps-cyan { color: #00FFFF; }
    .ps-white { color: #FFFFFF; }
    .ps-green { color: #00FF66; font-weight: bold; }
    .ps-red { color: #FF6666; font-weight: bold; }
    .ps-yellow { color: #FFFF00; font-weight: bold; }
    .ps-gray { color: #8F9D6A; }
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

# Cabeçalho PowerShell
st.markdown("""
<div style="border-bottom: 1px solid #7F9FBF; padding-bottom: 8px; margin-bottom: 15px;">
    <strong>Windows PowerShell</strong><br/>
    <span style="color: #A0B0C0;">Copyright (C) FactCheck Corporation. All rights reserved.</span><br/><br/>
    <span class="ps-prompt">PS C:\\Tools\\FactCheck&gt;</span> <span class="ps-white">Get-Help Invoke-FactCheck</span>
</div>
""", unsafe_allow_html=True)

# Seletor de parâmetros
modo = st.radio(
    "Selecionar modo de execução:",
    ["-Url (Verificar link de reportagem)", "-Text (Verificar declaração ou boato direto)"],
    label_visibility="collapsed"
)

if "-Url" in modo:
    url_input = st.text_input(
        "URL:",
        placeholder="PS C:\\> Invoke-FactCheck -Url https://g1.globo.com/...",
        label_visibility="collapsed"
    )
    executar = st.button("[ Enter ] Executar Análise", key="btn_run_url")

    if executar:
        if not url_input.strip():
            st.error("Erro de sintaxe: O parâmetro -Url não pode ser vazio.")
        else:
            with st.spinner("VERBOSE: Extraindo dados da URL e consultando DuckDuckGo/OpenAI..."):
                try:
                    st.session_state["resultado"] = use_case.execute_from_url(url_input)
                except Exception as e:
                    st.error(f"Erro de execução: {e}")

else:
    texto_input = st.text_area(
        "Texto:",
        placeholder="PS C:\\> Invoke-FactCheck -Text 'Cole aqui a alegação recebida em redes sociais...'",
        label_visibility="collapsed",
        height=100
    )
    executar = st.button("[ Enter ] Executar Análise", key="btn_run_text")

    if executar:
        if not texto_input.strip():
            st.error("Erro de sintaxe: O parâmetro -Text não pode ser vazio.")
        else:
            with st.spinner("VERBOSE: Buscando referências na web e validando coerência..."):
                try:
                    st.session_state["resultado"] = use_case.execute_from_text(texto_input)
                except Exception as e:
                    st.error(f"Erro de execução: {e}")

# Exibição dos resultados em formato tabela / dump do PowerShell
if "resultado" in st.session_state:
    res = st.session_state["resultado"]
    v_upper = res.verdict.upper()

    cor_classe = "ps-yellow"
    if "VERDADEIRO" in v_upper:
        cor_classe = "ps-green"
    elif "FALSO" in v_upper:
        cor_classe = "ps-red"

    st.markdown(f"""
    <div class="ps-output-box">
        <span class="ps-prompt">PS C:\\Tools\\FactCheck&gt;</span> <span class="ps-white">Format-Custom -View InspectionReport</span><br/><br/>
        <table style="width: 100%; border-collapse: collapse; color: #F1F1F1;">
            <tr style="border-bottom: 1px solid #7F9FBF;">
                <th style="text-align: left; padding: 4px;">Propriedade</th>
                <th style="text-align: left; padding: 4px;">Valor</th>
            </tr>
            <tr>
                <td style="padding: 6px; color: #00FFFF; width: 160px;">Verdict</td>
                <td style="padding: 6px;"><span class="{cor_classe}">[{v_upper}]</span></td>
            </tr>
            <tr>
                <td style="padding: 6px; color: #00FFFF;">ConfidenceScore</td>
                <td style="padding: 6px;">{res.confidence_score}%</td>
            </tr>
            <tr>
                <td style="padding: 6px; color: #00FFFF; vertical-align: top;">Summary</td>
                <td style="padding: 6px;">{res.summary}</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br/><span class='ps-prompt'>PS C:\\Tools\\FactCheck&gt;</span> <span class='ps-white'>Get-ExaminedClaims</span>", unsafe_allow_html=True)
    for i, claim in enumerate(res.key_claims, 1):
        st.markdown(f"<span style='color: #A0B0C0;'>[{i}]</span> {claim}", unsafe_allow_html=True)

    if res.sources_consulted:
        st.markdown("<br/><span class='ps-prompt'>PS C:\\Tools\\FactCheck&gt;</span> <span class='ps-white'>Get-ConsultedSources</span>", unsafe_allow_html=True)
        for source in res.sources_consulted:
            if source.startswith("http"):
                st.markdown(f"- <a href='{source}' target='_blank' style='color: #00FFFF; text-decoration: underline;'>{source}</a>", unsafe_allow_html=True)
            else:
                st.markdown(f"- <span style='color: #F1F1F1;'>{source}</span>", unsafe_allow_html=True)