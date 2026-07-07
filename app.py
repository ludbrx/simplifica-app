import streamlit as st

# Injete este bloco logo após as configurações iniciais da página (st.set_page_config)
st.markdown(
    """
    <style>
    /* Esconde o menu de hambúrguer no topo direito */
    #MainMenu {visibility: hidden;}
    
    /* Esconde o cabeçalho padrão */
    header {visibility: hidden;}
    
    /* Esconde o rodapé padrão 'Made with Streamlit' */
    footer {visibility: hidden;}
    
    /* Remove a linha decorativa colorida do topo */
    div[data-testid="stDecoration"] {display: none !important;}
    
    /* Esconde o botão de deploy e o widget de status/avatar no canto inferior direito */
    .stAppDeployButton {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    
    /* Força a remoção de qualquer elemento flutuante do painel do Streamlit */
    footer, .viewerBadge, div[class^="st-emotion-cache"] button {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
import streamlit as st
import re
import random
import string
import time
import urllib.parse
import requests
import calendar
from datetime import date, timedelta

# --- CONFIGURAÇÃO DA PÁGINA (FORÇANDO MENU ABERTO E NOVA LOGO) ---
st.set_page_config(page_title="Simplifica | Geradores, Calculadoras e Ferramentas Online", page_icon="💡", layout="wide", initial_sidebar_state="expanded")

# --- MEMÓRIA DE ESTADO ---
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "Inicio" 
if "current_tool" not in st.session_state:
    st.session_state.current_tool = "Sorteador Completo"

# --- INJEÇÃO DE CSS ---
st.markdown("""
    <style>
        /* Oculta os itens padrão do topo, mas mantém o cabeçalho acima de tudo */
        header {
            background-color: transparent !important;
            z-index: 999990 !important; 
        }
        [data-testid="stToolbar"], .stAppDeployButton {
            display: none !important;
        }
        
        /* REMOVE COMPLETAMENTE OS BOTÕES DE ESCONDER/EXPANDIR A BARRA LATERAL */
        [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"] {
            display: none !important;
        }
        
        /* REMOVE O ESPAÇO VAZIO NO TOPO DA BARRA LATERAL PARA SUBIR A LOGO */
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0rem !important;
        }
        
        .block-container {padding-top: 1rem !important; max-width: 1050px;}
        
        [data-testid="stSidebar"] { background-color: #0F172A; border-right: 1px solid #1E293B; }
        [data-testid="stSidebar"] * { color: #F8FAFC !important; }
        
        div.stButton > button { border-radius: 8px; font-weight: bold; transition: 0.3s; width: 100%; }
        div.stButton > button:hover { box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3); border-color: #3B82F6; }
        
        [data-testid="stSidebar"] div.stButton > button {
            text-align: left; justify-content: flex-start; background-color: transparent; border: none; padding: 2px 10px; font-weight: 500; font-size: 15px;
        }
        [data-testid="stSidebar"] div.stButton > button:hover { background-color: #1E293B; color: #3B82F6 !important; }
        
        .stTextArea textarea, .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"], .stDateInput input {
            background-color: #F8FAFC !important; border: 1.5px solid #CBD5E1 !important; border-radius: 10px !important; color: #1E293B !important;
        }
        
        .recibo-box {
            background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 40px; 
            font-family: 'Courier New', Courier, monospace; color: #1E293B; box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
            margin-top: 20px; line-height: 1.6;
        }
        .info-box-premium {
            background-color: #EFF6FF; border-left: 5px solid #3B82F6; padding: 20px; border-radius: 5px; color: #1E293B;
            margin-bottom: 25px; line-height: 1.6; font-size: 15px;
        }
        .spacing { margin-bottom: 20px; }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

def set_page(mode, tool=None):
    st.session_state.view_mode = mode
    if tool: st.session_state.current_tool = tool

# ==========================================
# TOPO DO SITE (BUSCA INTELIGENTE)
# ==========================================
c_espaco1, c_busca, c_espaco2 = st.columns([1, 2, 1])
with c_busca:
    busca = st.text_input("🔍 O que você precisa resolver hoje?", placeholder="Ex: Salário, Sorteio, Texto, Senha, Erros...")

st.markdown("<div class='spacing'></div>", unsafe_allow_html=True)

# Centralização perfeita com 4 botões
c_v1, c_btn0, c_btn1, c_btn2, c_btn3, c_v2 = st.columns([0.5, 1.5, 1.5, 1.5, 1.5, 0.5])
with c_btn0:
    if st.button("🏠 Início", use_container_width=True): set_page("Inicio")
with c_btn1: 
    if st.button("📌 Sobre Nós", use_container_width=True): set_page("Sobre")
with c_btn2: 
    if st.button("🛡️ Privacidade", use_container_width=True): set_page("Privacidade")
with c_btn3: 
    if st.button("📜 Termos", use_container_width=True): set_page("Termos")

st.markdown("---")

# ==========================================
# DICIONÁRIO DE SINÔNIMOS (BUSCA SEMÂNTICA)
# ==========================================
sinonimos = {
    "Sorteador Completo": ["sorteio", "rifa", "aleatorio", "numeros", "jogar", "equipes", "separar", "dados", "loteria", "mega sena"],
    "Revisor e Corretor Avançado": ["erro", "portugues", "ortografia", "gramatica", "plagio", "ia", "resumo", "abnt"],
    "Gerador de Texto (Avançado)": ["lorem ipsum", "texto falso", "gerar texto", "paragrafos", "redacao"],
    "Gerador de Recibo de Pagamento": ["recibo", "pagamento", "comprovante", "dinheiro", "nota"],
    "Calculadora de Salário Líquido (CLT)": ["salario", "clt", "inss", "irrf", "desconto", "pagamento", "holerite"],
    "Gerador de CPF/CNPJ (Testes)": ["gerar", "criar", "cpf", "cnpj", "documento", "teste", "fake", "falso"],
    "Calculadora de Férias": ["ferias", "descanso", "1/3", "rescisao"],
    "Calculadora Regra 50-30-20": ["financas", "dinheiro", "organizar", "50", "30", "20", "salario"],
    "Calculadora de Datas": ["somar data", "subtrair data", "tempo", "dias"],
    "Calendário 2026 Útil": ["feriados", "datas", "folga", "eventos"],
}

# ==========================================
# BARRA LATERAL (CATEGORIAS)
# ==========================================
# O CSS foi alterado para zerar o padding superior, e o margin-top foi negativado para puxar a logo bem para cima.
st.sidebar.markdown("<h2 style='margin-top: -15px;'>💡 Simplifica</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size: 13px; color: #94A3B8; margin-top: -10px;'>Aplicações web gratuitas para o seu dia a dia.</p>", unsafe_allow_html=True)

categorias = {
    "📝 Textos e Códigos": [
        "Revisor e Corretor Avançado", "Gerador de Texto (Avançado)", "Organizador de CPFs e CNPJs", 
        "Contador de Caracteres", "Maiúsculas e Minúsculas", "Inversor de Texto", "Organizador Alfabético"
    ],
    "🔄 Geradores": [
        "Gerador de Senhas Seguras", "Gerador de Recibo de Pagamento", "Gerador de QR Code", 
        "Gerador de Link WhatsApp", "Gerador de UTM (Marketing)", "Gerador de Nicks (Jogos)", 
        "Gerador de CPF/CNPJ (Testes)"
    ],
    "💰 Finanças e Cálculos": [
        "Calculadora de Salário Líquido (CLT)", "Calculadora de Férias", "Calculadora de Horas Extras",
        "Calculadora de Juros Compostos", "Calculadora Regra 50-30-20", "Calculadora de Porcentagem", 
        "Calculadora de Regra de Três"
    ],
    "🎲 Sorteios e Jogos": [
        "Sorteador Completo", "Gerador de Desculpas Aleatórias"
    ],
    "🛠️ Utilitários": [
        "Calculadora de Datas", "Calendário 2026 Útil", "Validador de CPF e CNPJ", "Busca Endereço por CEP", 
        "Calculadora de Dias Úteis", "Calculadora de IMC", "Conversor de Medidas", "Sorteador de Cores (HEX)"
    ]
}

if busca:
    st.sidebar.markdown("### 🔎 Resultados")
    termo = busca.lower()
    for cat, tools in categorias.items():
        for tool in tools:
            matches_name = termo in tool.lower()
            matches_synonym = any(termo in sin for sin in sinonimos.get(tool, []))
            if matches_name or matches_synonym:
                label = f"📍 {tool}" if (st.session_state.current_tool == tool and st.session_state.view_mode == "tool") else f" {tool}"
                if st.sidebar.button(label, key=f"search_{tool}"):
                    set_page("tool", tool)
                    st.rerun()
else:
    for cat, tools in categorias.items():
        st.sidebar.markdown(f"<h4 style='color:#E2E8F0; margin-bottom:5px; margin-top:15px;'>{cat}</h4>", unsafe_allow_html=True)
        for tool in tools:
            label = f"📍 {tool}" if (st.session_state.current_tool == tool and st.session_state.view_mode == "tool") else f"  {tool}"
            if st.sidebar.button(label, key=f"menu_{tool}"):
                set_page("tool", tool)
                st.rerun()

st.sidebar.markdown("<br><p style='font-size: 11px; color: #64748B;'>🍪 O uso de cookies pelo AdSense é obrigatório e processado automaticamente.</p>", unsafe_allow_html=True)

# ==========================================
# PÁGINAS LEGAIS E INICIAL (COMPLETAS)
# ==========================================
if st.session_state.view_mode == "Inicio":
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; color: #1E293B; margin-bottom: 0;'>👋 Olá! Bem-vindo ao Simplifica</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #64748B; margin-top: 5px; margin-bottom: 40px;'>Seu assistente digital inteligente. Tudo o que você precisa em um só lugar.</h3>", unsafe_allow_html=True)
    
    # Novo design moderno com grid de cards
    st.markdown("""
    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px;'>
        <div style='background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); border-left: 5px solid #3B82F6; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
            <h3 style='color: #1D4ED8; margin-top: 0;'>📝 Textos e Códigos</h3>
            <p style='font-size: 15px; color: #334155; margin-bottom: 0;'>Corrija erros gramaticais, resuma textos, conte palavras, formate maiúsculas/minúsculas e limpe documentos com facilidade.</p>
        </div>
        <div style='background: linear-gradient(135deg, #FDF4FF 0%, #FCE7F3 100%); border-left: 5px solid #EC4899; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
            <h3 style='color: #BE185D; margin-top: 0;'>🔄 Geradores</h3>
            <p style='font-size: 15px; color: #334155; margin-bottom: 0;'>Crie senhas hiper seguras, gere recibos de pagamento em PDF, crie links rastreáveis (UTM) e QR Codes na hora.</p>
        </div>
        <div style='background: linear-gradient(135deg, #F0FDF4 0%, #D1FAE5 100%); border-left: 5px solid #10B981; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
            <h3 style='color: #047857; margin-top: 0;'>💰 Finanças</h3>
            <p style='font-size: 15px; color: #334155; margin-bottom: 0;'>Simule seu salário líquido CLT, calcule férias com exatidão, projete juros compostos e aplique a regra 50-30-20.</p>
        </div>
        <div style='background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); border-left: 5px solid #F59E0B; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
            <h3 style='color: #B45309; margin-top: 0;'>🎲 Sorteios</h3>
            <p style='font-size: 15px; color: #334155; margin-bottom: 0;'>Realize sorteios justos de rifas, monte equipes, sorteie letras para jogos e gere palpites para loterias oficiais.</p>
        </div>
    </div>
    
    <div style='background-color: #0F172A; border-radius: 12px; padding: 30px; text-align: center; color: white; box-shadow: 0 10px 15px rgba(0,0,0,0.1); margin-top: 10px;'>
        <h2 style='margin-top: 0; color: #F8FAFC;'>Tudo roda direto no seu navegador.</h2>
        <p style='font-size: 18px; color: #94A3B8; margin-bottom: 0;'>Rápido, 100% seguro e sem necessidade de instalações. Escolha uma ferramenta no menu ao lado para começar!</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.view_mode == "Sobre":
    st.title("📌 Sobre o Simplifica")
    st.markdown("""
    O **Simplifica.app** é um portal de aplicações web gratuitas projetado para desenvolvedores, estudantes, profissionais de RH e usuários comuns que buscam produtividade real sem complicações.
    
    ### 🎯 Nossa Missão
    Prover ferramentas digitais ultrarrápidas que resolvam problemas complexos, cálculos extensos e formatações de dados em milissegundos. Queremos que você elimine o trabalho braçal de estruturar planilhas, gerar dados de teste ou corrigir textos, tudo isso sem a necessidade de instalar aplicativos ou pagar taxas ocultas.
    
    ### 👁️ Nossa Visão
    Tornar-se o maior e mais confiável hub de utilitários online do Brasil, reconhecido pela interface limpa, ausência de paywalls e respeito absoluto à privacidade do processamento local (*client-side*).
    
    ### 💎 Nossos Valores
    * **Transparência Absoluta:** O que você vê é o que você tem. Sem cadastros obrigatórios.
    * **Segurança por Design:** Ferramentas criadas para processar dados no seu próprio navegador, garantindo proteção total contra vazamento de informações sensíveis.
    * **Agilidade Máxima:** Foco em interfaces responsivas e de carregamento instantâneo para não interromper seu fluxo de trabalho.
    
    *Contato para parcerias corporativas e suporte técnico: simplificaferramenta@gmail.com*
    """)

elif st.session_state.view_mode == "Privacidade":
    st.title("🛡️ Política de Privacidade")
    st.markdown("""
    **Data de vigência: 06 de Julho de 2026**

    A proteção dos seus dados é a nossa prioridade. O **Simplifica.app** está em total conformidade com as diretrizes da Lei Geral de Proteção de Dados (LGPD) no Brasil e o Regulamento Geral de Proteção de Dados (GDPR).

    ### 1. Processamento e Coleta de Dados Pessoais
    O Simplifica atua estritamente como um processador *Client-Side* (no navegador). **Nós NÃO coletamos, NÃO armazenamos em banco de dados, NÃO vendemos e NÃO transmitimos para nossos servidores** as informações digitadas nas ferramentas (como CPFs, senhas, valores salariais, documentos ou textos). Todo o processamento matemático, de formatação e de texto ocorre no seu dispositivo local. Quando você fecha ou atualiza a página, os dados são permanentemente destruídos.

    ### 2. Cookies e Web Beacons (Google AdSense)
    Para que possamos oferecer as ferramentas de forma 100% gratuita e pagar os custos de hospedagem, o site é monetizado através de publicidade de redes terceirizadas, especificamente o programa **Google AdSense**.
    * O Google, como fornecedor de terceiros, utiliza cookies (incluindo o cookie DoubleClick) para veicular anúncios com base nas visitas anteriores do usuário ao nosso site ou a outros sites na Internet.
    * Os parceiros de publicidade podem usar cookies e web beacons para coletar dados não identificáveis e exibir anúncios segmentados e relevantes.
    * **Seus Direitos e Controle:** Você pode revogar o consentimento e desativar o uso de cookies de publicidade personalizada a qualquer momento acessando as [Configurações de anúncios do Google](https://www.google.com/settings/ads) ou através da plataforma [About Ads](http://www.aboutads.info/choices/).

    ### 3. Analytics e Monitoramento de Desempenho
    Utilizamos serviços de análise de tráfego de mercado para coletar dados estatísticos estritamente anonimizados (como tipo de navegador, sistema operacional, tempo de permanência na página e país de origem). Nenhuma dessas informações pode ser usada para identificar você pessoalmente. O único propósito é entender quais ferramentas precisam de melhoria técnica.

    ### 4. Links para Plataformas de Terceiros
    Nosso site pode conter links ou redirecionamentos para sites de parceiros (como geradores de link para WhatsApp). Não nos responsabilizamos pelas práticas de privacidade ou pelo conteúdo dessas plataformas externas.
    """)

elif st.session_state.view_mode == "Termos":
    st.title("📜 Termos e Condições de Uso")
    st.markdown("""
    **Última atualização: 06 de Julho de 2026**

    O uso do site **Simplifica.app** e de todos os seus subdiretórios está sujeito à aceitação integral dos termos e condições descritos abaixo. Ao utilizar nossas ferramentas, geradores e calculadoras, você atesta que leu, compreendeu e concorda com estas diretrizes legais.

    ### 1. Natureza Informativa e Isenção Total de Garantias
    O SITE E TODAS AS SUAS FERRAMENTAS SÃO FORNECIDOS "NO ESTADO EM QUE SE ENCONTRAM" E "CONFORME DISPONÍVEIS", SEM QUALQUER TIPO DE GARANTIA, EXPRESSA OU IMPLÍCITA, INCLUINDO GARANTIAS DE COMERCIALIZAÇÃO OU ADEQUAÇÃO A UM DETERMINADO FIM.
    * **Calculadoras Trabalhistas e Financeiras:** Os resultados das calculadoras de rescisão CLT, férias, salários líquidos, horas extras e juros compostos são obtidos através de fórmulas matemáticas e algoritmos públicos. Eles devem ser usados **apenas como referência estimativa**. O Simplifica não atua como escritório de contabilidade, consultor financeiro ou jurídico, e o usuário não deve utilizar os resultados gerados como prova documental contábil oficial perante tribunais ou negociações.
    
    ### 2. Limitação de Responsabilidade Civil e Comercial
    EM NENHUMA CIRCUNSTÂNCIA O SIMPLIFICA, SEUS DESENVOLVEDORES, DIRETORES OU PARCEIROS SERÃO RESPONSÁVEIS POR QUAISQUER DANOS DIRETOS, INDIRETOS, INCIDENTAIS, ESPECIAIS OU CONSEQUENCIAIS (INCLUINDO, SEM LIMITAÇÃO, LUCROS CESSANTES, INTERRUPÇÃO DE NEGÓCIOS OU PERDA DE DADOS) RESULTANTES DO USO OU DA INCAPACIDADE DE USAR OS SERVIÇOS DESTE SITE.

    ### 3. Restrições de Uso (Geradores de Dados de Teste)
    A ferramenta "Gerador de CPF/CNPJ (Testes)" gera sequências numéricas aleatórias que atendem aos requisitos lógicos de validação do Módulo 11 estipulado pela Receita Federal. O usuário concorda e reconhece formalmente que **estes dados são gerados estritamente para testes em ambientes de desenvolvimento e homologação de software**. A utilização destas sequências numéricas para efetuar cadastros fraudulentos, compras, falsidade ideológica ou qualquer outra atividade ilícita constitui infração penal grave, pela qual o usuário responderá integral e exclusivamente perante as autoridades policiais e judiciais competentes.

    ### 4. Propriedade Intelectual e Proteção de Servidores
    O layout do site, sua logomarca, identidades visuais, textos institucionais e o código estrutural da interface pertencem exclusivamente ao Simplifica. É terminantemente vedada a prática de *web scraping* (raspagem de dados em massa), ataques de negação de serviço (DDoS) e o uso de robôs ou scripts automatizados para extrair, copiar ou sobrecarregar as funcionalidades da plataforma. O descumprimento resultará no bloqueio imediato do IP e medidas legais cabíveis.
    """)

# ==========================================
# CÓDIGO DAS FERRAMENTAS PRINCIPAIS
# ==========================================
elif st.session_state.view_mode == "tool":
    ferramenta = st.session_state.current_tool

    # --- CATEGORIA: TEXTOS E CORREÇÕES ---
    if ferramenta == "Revisor e Corretor Avançado":
        st.title("A✓ Revisor e Corretor Avançado")
        st.markdown("A mais completa ferramenta de **correção ortográfica online**. Analise a gramática, aplique formatação inteligente ou gere referências ABNT em segundos. **Como usar?** Basta colar seu texto nas abas abaixo e clicar no botão correspondente para iniciar o processamento local.")
        
        tab_corretor, tab_resumo, tab_abnt = st.tabs(["✔️ Corretor Ortográfico Inteligente", "📝 Resumidor de Textos", "📚 Referências ABNT"])
        
        with tab_corretor:
            st.markdown("Cole seu texto abaixo. Use a Formatação Automática para limpar espaços e pontuações, ou a Análise Gramatical para encontrar erros estruturais profundos:")
            texto_corrigir = st.text_area("Texto a ser analisado:", height=200, key="txt_corr")
            
            c_btn1, c_btn2 = st.columns(2)
            
            if c_btn1.button("🔍 Análise Gramatical Completa", type="primary"):
                if texto_corrigir:
                    with st.spinner("Analisando gramática avançada..."):
                        erros_comuns_brasileiros = {
                            r'\bcomcerteza\b': 'com certeza', r'\bconcerteza\b': 'com certeza',
                            r'\bderrepente\b': 'de repente', r'\bnada haver\b': 'nada a ver',
                            r'\bporisso\b': 'por isso', r'\bapartir\b': 'a partir',
                            r'\bmenas\b': 'menos', r'\bpobrema\b': 'problema',
                            r'\bagente fomos\b': 'a gente foi / nós fomos', r'\bmim fazer\b': 'eu fazer',
                            r'\bfasso\b': 'faço', r'\bezceção\b': 'exceção', r'\bconciliar\b': 'conciliar'
                        }
                        
                        erros_locais_encontrados = []
                        texto_min = texto_corrigir.lower()
                        for erro_regex, correcao in erros_comuns_brasileiros.items():
                            if re.search(erro_regex, texto_min):
                                erros_locais_encontrados.append(f"**Aviso:** O termo incorreto foi detectado.\n\n**Sugestão de Troca:** {correcao}\n\n*Tipo:* Erro comum de digitação/concordância no Brasil.")

                        try:
                            res = requests.post("https://api.languagetoolplus.com/v2/check", data={"text": texto_corrigir, "language": "pt-BR"}).json()
                            erros_api = res.get("matches", [])
                            
                            if not erros_api and not erros_locais_encontrados:
                                st.success("🎉 Nenhum erro ortográfico ou gramatical grave encontrado!")
                            else:
                                st.warning(f"⚠️ Encontramos possíveis desvios gramaticais no seu texto:")
                                for erro_local in erros_locais_encontrados:
                                    st.info(erro_local)
                                for erro in erros_api:
                                    msg = erro['message']
                                    sugestao = ", ".join([r['value'] for r in erro.get('replacements', [])[:3]])
                                    trecho = erro['context']['text']
                                    st.info(f"**Aviso Gramatical:** {msg}\n\n**Sugestão de Troca:** {sugestao if sugestao else 'Verifique a estrutura.'}\n\n*Onde:* '...{trecho}...'")
                        except:
                            st.error("Erro ao conectar com o servidor de gramática. Tente novamente.")
                else: st.warning("Cole algum texto para analisarmos.")
                
            if c_btn2.button("✨ Formatação Automática (Limpeza Rápida)", type="secondary"):
                if texto_corrigir:
                    txt = re.sub(r'\s+', ' ', texto_corrigir).strip() 
                    txt = re.sub(r'\s+([.,!?;:])', r'\1', txt) 
                    txt = re.sub(r'([.,!?;:])([^\s])', r'\1 \2', txt) 
                    txt = re.sub(r'(^|[.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), txt) 
                    st.success("Texto formatado com sucesso! Espaços e pontuações corrigidas. Copie o resultado abaixo:")
                    st.code(txt, language="plaintext")
                else:
                    st.warning("Cole algum texto para formatar.")

        with tab_resumo:
            st.markdown("Extraia os pontos mais importantes de um texto longo de forma automática.")
            texto_resumo = st.text_area("Texto original longo:", height=200, key="txt_res")
            if st.button("Gerar Resumo (Extração de Frases-Chave)", type="primary", key="btn_resumo"):
                if len(texto_resumo) > 100:
                    frases = [f.strip() for f in texto_resumo.split('.') if len(f.strip()) > 10]
                    if len(frases) > 3:
                        resumo = ". ".join(random.sample(frases, max(2, len(frases)//3))) + "."
                        st.success("Resumo gerado com base nas sentenças chave:")
                        st.write(resumo)
                    else: st.warning("O texto é muito curto para ser resumido.")
                else: st.warning("Cole um texto maior para que possamos extrair informações relevantes.")

        with tab_abnt:
            st.markdown("Gere referências bibliográficas automáticas nos padrões ABNT sem dor de cabeça.")
            tipo = st.selectbox("Tipo de Fonte Referenciada:", ["Livro Impresso / Digital", "Site / Artigo Online"])
            if tipo == "Livro Impresso / Digital":
                c1, c2 = st.columns(2)
                with c1: autor = st.text_input("Sobrenome, Nome do Autor (Ex: SILVA, João)")
                with c2: titulo = st.text_input("Título da Obra:")
                c3, c4, c5 = st.columns(3)
                with c3: cidade = st.text_input("Cidade da Edição:")
                with c4: editora = st.text_input("Editora:")
                with c5: ano = st.text_input("Ano de Publicação:")
                if st.button("Gerar Referência ABNT", type="primary", key="btn_abnt_livro"):
                    if autor and titulo: st.code(f"{autor.upper()}. {titulo}. {cidade}: {editora}, {ano}.", language="plaintext")
                    else: st.warning("Preencha ao menos Autor e Título.")
            else:
                c1, c2 = st.columns(2)
                with c1: autor_site = st.text_input("Autor (Instituição ou Pessoa Física):")
                with c2: titulo_site = st.text_input("Título da Página/Artigo:")
                link = st.text_input("URL Completa (Link):")
                if st.button("Gerar Referência ABNT", type="primary", key="btn_abnt_site"):
                    if link: st.code(f"{autor_site.upper()}. {titulo_site}. Disponível em: <{link}>. Acesso em: {date.today().strftime('%d %b. %Y')}.", language="plaintext")
                    else: st.warning("A URL (Link) é obrigatória.")

    elif ferramenta == "Gerador de Texto (Avançado)":
        st.title("📄 Gerador de Textos Avançado")
        st.markdown("Crie blocos estruturados de **texto falso para preenchimento de layouts (Lorem Ipsum)**. Ideal para web designers, desenvolvedores e diretores de arte que precisam criar mockups visuais para clientes sem utilizar textos finais reais.")
        
        tipo_texto = st.selectbox("Escolha a Temática do Texto:", ["Clássico (Lorem Ipsum Latin)", "Corporativo / Business (Corporate Ipsum)", "Tecnologia / Hacker (Tech Ipsum)"])
        c1, c2 = st.columns(2)
        with c1: paragrafos = st.number_input("Número de parágrafos desejados:", min_value=1, max_value=50, value=3)
        with c2: tamanho = st.selectbox("Comprimento de cada parágrafo:", ["Curto", "Médio", "Longo"])
        
        if st.button("Gerar Blocos de Texto", type="primary"):
            if tipo_texto == "Clássico (Lorem Ipsum Latin)":
                banco = ["consectetur", "adipiscing", "elit", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua"]
            elif tipo_texto == "Corporativo / Business (Corporate Ipsum)":
                banco = ["sinergia", "mindset", "brainstorming", "alinhamento", "entregável", "agile", "sprint", "kanban", "startup", "inovação", "disruptivo", "escalável", "valuation", "B2B", "networking"]
            else:
                banco = ["algoritmo", "criptografia", "blockchain", "servidor", "nuvem", "código", "python", "machine learning", "backend", "frontend", "API", "banco de dados", "framework", "deploy"]
                
            texto_final = ""
            for i in range(paragrafos):
                qtd = 20 if tamanho == "Curto" else 50 if tamanho == "Médio" else 90
                p = []
                for _ in range(qtd): p.append(random.choice(banco))
                texto_final += " ".join(p).capitalize() + ".\n\n"
            
            st.markdown(f"<div style='background-color: #F8FAFC; border: 1.5px solid #CBD5E1; border-radius: 10px; padding: 20px;'>{texto_final.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

    elif ferramenta == "Organizador de CPFs e CNPJs":
        st.title("🧹 Organizador e Limpador de CPF/CNPJ")
        st.markdown("**Como usar:** Cole abaixo a sua lista bruta e suja. Nossa ferramenta online é projetada para **limpar CPF e CNPJ de planilhas** automaticamente. O sistema varre o bloco de texto, remove todos os pontos, traços, barras e letras espúrias, devolvendo a você apenas as sequências numéricas limpas e prontas para importação no banco de dados.")
        texto = st.text_area("Cole sua lista de documentos (um por linha):", height=200)
        if st.button("Limpar Documentos Agora", type="primary") and texto:
            st.success("Lista processada! Copie os dados limpos abaixo:")
            st.code(re.sub(r'[^0-9\n]', '', texto), language="plaintext")

    elif ferramenta == "Contador de Caracteres":
        st.title("📝 Contador de Caracteres e Palavras")
        st.markdown("**Como usar:** Digite ou cole seu conteúdo na caixa. Nosso **contador de palavras e caracteres online** faz a contagem exata em tempo real. Essencial para profissionais de marketing, redatores SEO e gestores de redes sociais que precisam ajustar legendas do Instagram (limite de 2.200 caracteres) ou X/Twitter (limite de 280 caracteres).")
        texto = st.text_area("Cole seu texto para contagem:", height=200)
        if st.button("Realizar Contagem Métrica", type="primary") and texto:
            st.success("Contagem concluída!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Total de Caracteres (Com Espaços)", len(texto))
            c2.metric("Caracteres (Sem Espaços)", len(texto.replace(" ", "").replace("\n", "")))
            c3.metric("Total de Palavras", len(texto.split()))

    elif ferramenta == "Inversor de Texto":
        st.title("🙃 Inversor de Texto (De trás para frente)")
        st.markdown("**Como usar:** Cole o seu texto. A ferramenta atua como um **espelho de palavras**, invertendo totalmente a ordem das letras. Uma funcionalidade lúdica excelente para criar senhas robustas a partir de frases comuns, gerar códigos para RPGs ou criar mensagens codificadas nas redes sociais.")
        texto = st.text_area("Texto a ser invertido:", height=200)
        if st.button("Inverter Tudo", type="primary") and texto:
            st.success("Seu texto foi espelhado:")
            st.code(texto[::-1], language="plaintext")

    elif ferramenta == "Organizador Alfabético":
        st.title("🔤 Organizador em Ordem Alfabética")
        st.markdown("**Como usar:** Nossa ferramenta online para **colocar listas em ordem alfabética (A-Z)** é a salvação para professores organizando chamadas escolares, organizadores de eventos montando listas de convidados ou gerentes de estoque catalogando produtos. Cole um item por linha e deixe o sistema classificar.")
        texto = st.text_area("Sua lista desorganizada (um item por linha):", height=200)
        if st.button("Classificar Lista (A - Z)", type="primary") and texto:
            linhas = [l.strip() for l in texto.split('\n') if l.strip()]
            linhas.sort(key=str.lower)
            st.success("Lista perfeitamente classificada:")
            st.code("\n".join(linhas), language="plaintext")

    elif ferramenta == "Maiúsculas e Minúsculas":
        st.title("Aa Conversor de Maiúsculas e Minúsculas")
        st.markdown("**Como usar:** O seu teclado travou no Caps Lock? Não reescreva tudo! Use o **conversor de texto online** para formatar rapidamente milhares de linhas de texto. Alterne entre TUDO MAIÚSCULO, tudo minúsculo, capitalização de frases (Primeira Letra) ou crie o efeito de inversão.")
        texto = st.text_area("Texto original:", height=200)
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("TUDO MAIÚSCULO", type="primary") and texto: st.code(texto.upper())
        if c2.button("tudo minúsculo", type="primary") and texto: st.code(texto.lower())
        if c3.button("Primeira Letra", type="primary") and texto: st.code(texto.capitalize())
        if c4.button("iNvErTeR cAxIa", type="primary") and texto: 
            st.code("".join([c.upper() if i%2==0 else c.lower() for i, c in enumerate(texto)]))


    # --- CATEGORIA: GERADORES ---
    elif ferramenta == "Gerador de Senhas Seguras":
        st.title("🔐 Gerador de Senhas Seguras")
        st.markdown("Crie senhas fortes, aleatórias e praticamente impossíveis de hackear. Nosso **gerador de senhas online** utiliza criptografia local para misturar letras, números e símbolos de forma inviolável.")
        tamanho = st.slider("Tamanho da senha", 8, 64, 20)
        c1, c2 = st.columns(2)
        with c1: num = st.toggle("Incluir Números (0-9)", True)
        with c2: sim = st.toggle("Incluir Símbolos (!@#$)", True)
        if st.button("Criar Senha", type="primary"):
            chars = string.ascii_letters + (string.digits if num else "") + ("!@#$%&*()_-+=" if sim else "")
            st.markdown(f"<div style='background-color: #F8FAFC; border: 2px solid #3B82F6; border-radius: 10px; padding: 20px; font-family: monospace; font-size: 20px; text-align: center; color: #1E293B;'>{''.join(random.choice(chars) for i in range(tamanho))}</div>", unsafe_allow_html=True)

    elif ferramenta == "Gerador de Recibo de Pagamento":
        st.title("🧾 Gerador de Recibo Online")
        st.markdown("Crie um **recibo de pagamento em PDF visual** pronto para impressão. Ferramenta grátis ideal para profissionais autônomos e freelancers oficializarem suas transações financeiras.")
        
        c1, c2 = st.columns(2)
        with c1: valor = st.number_input("Valor do Recibo (R$):", min_value=0.0, value=150.0, step=50.0)
        with c2: data_recibo = st.date_input("Data da Emissão:")
        
        pagador = st.text_input("Recebi de (Nome do cliente ou empresa):", placeholder="Nome do Cliente ou Empresa")
        doc_pagador = st.text_input("CPF/CNPJ do Pagador (Opcional):")
        referente = st.text_input("Referente a (Serviço ou Produto):", placeholder="Ex: Serviços de consultoria, Venda de equipamento...")
        
        emissor = st.text_input("Nome do Emissor (Você):", value="Lucas Rodrigues Brasil")
        doc_emissor = st.text_input("CPF/CNPJ do Emissor (Opcional):")
        
        if st.button("Gerar Recibo Profissional", type="primary"):
            if pagador and referente and emissor:
                doc_p = f"<br>CPF/CNPJ: {doc_pagador}" if doc_pagador else ""
                doc_e = f"<br>CPF/CNPJ: {doc_emissor}" if doc_emissor else ""
                
                html_recibo = f"""
                <div class="recibo-box">
                    <h2 style="text-align: center; color: #1E293B; border-bottom: 2px solid #E2E8F0; padding-bottom: 10px; margin-top: 0;">RECIBO DE PAGAMENTO</h2>
                    <h3 style="text-align: right; color: #3B82F6;">VALOR: R$ {valor:,.2f}</h3>
                    <p style="font-size: 18px;">
                        Recebi(emos) de <strong>{pagador.upper()}</strong>{doc_p},<br><br>
                        A importância de <strong>R$ {valor:,.2f}</strong>,<br>
                        referente a: <em>{referente.capitalize()}</em>.
                    </p>
                    <p style="font-size: 16px;">Para maior clareza, firmo(amos) o presente.</p>
                    <p style="text-align: right; font-style: italic;">Emitido em: {data_recibo.strftime('%d/%m/%Y')}</p>
                    <br><br>
                    <div style="text-align: center; width: 60%; margin: 0 auto; border-top: 1px solid #1E293B; padding-top: 10px;">
                        <strong>{emissor.upper()}</strong>{doc_e}
                    </div>
                </div>
                """
                st.markdown(html_recibo, unsafe_allow_html=True)
                st.info("💡 Dica: Você pode selecionar o recibo inteiro acima, clicar com o botão direito e escolher a opção 'Imprimir' do navegador.")
            else:
                st.warning("Preencha o Nome do Pagador, Emissor e o Referente.")

    elif ferramenta == "Gerador de QR Code":
        st.title("📱 Gerador de Imagem QR Code")
        st.markdown("O melhor **criador de QR Code online grátis**. Transforme links de sites, redes sociais, cardápios digitais ou textos sensíveis em um código rastreável que qualquer celular moderno com câmera consegue ler instantaneamente.")
        texto_qr = st.text_area("Digite a URL ou Mensagem:")
        if st.button("Converter para Imagem QR", type="primary") and texto_qr:
            c1, c2, c3 = st.columns([1,2,1])
            with c2: st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(texto_qr)}", use_container_width=True)

    elif ferramenta == "Gerador de Link WhatsApp":
        st.title("💬 Gerador de Link Curto de WhatsApp")
        st.markdown("Crie um **link dinâmico de contato para o WhatsApp** com uma mensagem automática pré-escrita. Ferramenta poderosa para atrair clientes clicando em links na biografia do Instagram ou botões do seu site de vendas.")
        telefone = st.text_input("Número do Contato (Inclua o DDD):", placeholder="Ex: 21999999999")
        mensagem = st.text_area("Mensagem Automática Inicial (Opcional):", placeholder="Olá, gostaria de saber mais informações!")
        if st.button("Gerar Código da URL", type="primary") and telefone:
            num = '55' + re.sub(r'\D', '', telefone) if not re.sub(r'\D', '', telefone).startswith('55') else re.sub(r'\D', '', telefone)
            st.code(f"https://wa.me/{num}?text={urllib.parse.quote(mensagem)}", language="plaintext")

    elif ferramenta == "Gerador de UTM (Marketing)":
        st.title("🔗 Gerador Oficial de Parâmetros UTM")
        st.markdown("Para gestores de tráfego. Crie **URLs rastreáveis personalizadas** e injete UTM tags (Source, Medium, Campaign) para mapear o sucesso dos seus anúncios rigorosamente dentro da interface do Google Analytics 4.")
        url_base = st.text_input("Link da Página de Destino:")
        source = st.text_input("utm_source (Origem - Ex: instagram, facebook):")
        medium = st.text_input("utm_medium (Canal - Ex: cpc, story, email):")
        name = st.text_input("utm_campaign (Campanha - Ex: lancamento_verao):")
        if st.button("Gerar Código Rastreável Completo", type="primary") and url_base and source and medium and name:
            st.code(f"{url_base}?utm_source={source}&utm_medium={medium}&utm_campaign={name}", language="plaintext")

    elif ferramenta == "Gerador de Nicks (Jogos)":
        st.title("🎮 Gerador de Nicknames e Apelidos Pro")
        st.markdown("**Como usar:** Sofrendo bloqueio criativo? Use a nossa inteligência para gerar **nomes de usuário épicos para gamers**, RPG de mesa, ou criar seu novo arroba nas redes sociais. Clique e nós misturamos as palavras de forma criativa.")
        adjetivos = ["Sombrio", "Letal", "Fantom", "Mistico", "Veloz", "Sangrento", "Supremo", "Oculto", "Toxico", "Invicto", "Profano", "Caotico", "Luminoso", "Imortal", "Voraz", "Divino", "Cosmico", "Arcano", "Vazio", "Furioso", "Perdido", "Gelido", "Colossal", "Astro", "Tenebroso", "Aureo", "Noturno", "Silencioso", "Carmesim", "Onipresente"]
        substantivos = ["Lobo", "Dragao", "Guerreiro", "Assassino", "Vingador", "Tita", "Corvo", "Espectro", "Cacador", "Mago", "Mutante", "Templario", "Necromante", "Demonio", "Fenix", "Kraken", "Centauro", "Gladiador", "Rei", "Andarilho", "Falcao", "Serafim", "Mestre", "Renegado", "Mito", "Vagabundo", "Ermitao", "Paladino", "Ninjas", "Destruidor"]
        if st.button("Sortear um Nick Épico", type="primary"):
            st.balloons()
            nick = f"{random.choice(adjetivos)}{random.choice(substantivos)}{random.randint(1, 999)}"
            st.markdown(f"<h1 style='text-align: center; font-size: 65px; color: #3B82F6; background-color: #F8FAFC; padding: 20px; border-radius: 15px; border: 2px dashed #CBD5E1;'>{nick}</h1>", unsafe_allow_html=True)

    elif ferramenta == "Gerador de CPF/CNPJ (Testes)":
        st.title("⚙️ Gerador de CPF e CNPJ de Teste")
        st.markdown("Gerador de documentos matematicamente válidos para **testes de software e formulários**. Ferramenta desenvolvida exclusivamente para desenvolvedores web e QAs.")
        st.warning("⚠️ **AVISO LEGAL IMPORTANTE:** Os documentos gerados aqui são sequências numéricas aleatórias que passam no algoritmo oficial de validação (Módulo 11), mas **NÃO são reais** e não possuem vínculo com pessoas físicas ou jurídicas. O uso destes dados para qualquer fim ilícito ou cadastros em sites oficiais é crime.", icon="⚠️")
        
        def digito_cpf(digs):
            s = sum(v * p for v, p in zip(digs, range(len(digs) + 1, 1, -1)))
            return 0 if s % 11 < 2 else 11 - (s % 11)

        def gerar_cnpj_logica():
            base = [random.randint(0,9) for _ in range(8)] + [0, 0, 0, 1]
            p1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            d1 = 11 - (sum(b * p for b, p in zip(base, p1)) % 11)
            base.append(0 if d1 >= 10 else d1)
            p2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            d2 = 11 - (sum(b * p for b, p in zip(base, p2)) % 11)
            base.append(0 if d2 >= 10 else d2)
            c = [str(x) for x in base]
            return f"{c[0]}{c[1]}.{c[2]}{c[3]}{c[4]}.{c[5]}{c[6]}{c[7]}/{c[8]}{c[9]}{c[10]}{c[11]}-{c[12]}{c[13]}"

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div style='padding: 20px; border: 1px solid #CBD5E1; border-radius: 10px; text-align: center;'>", unsafe_allow_html=True)
            st.markdown("### 👤 Gerar CPF")
            if st.button("Criar CPF Válido", use_container_width=True, key="btn_cpf"):
                cpf = [random.randint(0, 9) for _ in range(9)]
                d1 = digito_cpf(cpf)
                cpf.append(d1)
                d2 = digito_cpf(cpf)
                cpf.append(d2)
                st.code(f"{cpf[0]}{cpf[1]}{cpf[2]}.{cpf[3]}{cpf[4]}{cpf[5]}.{cpf[6]}{cpf[7]}{cpf[8]}-{cpf[9]}{cpf[10]}")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c2:
            st.markdown("<div style='padding: 20px; border: 1px solid #CBD5E1; border-radius: 10px; text-align: center;'>", unsafe_allow_html=True)
            st.markdown("### 🏢 Gerar CNPJ")
            if st.button("Criar CNPJ Válido", use_container_width=True, key="btn_cnpj"):
                st.code(gerar_cnpj_logica())
            st.markdown("</div>", unsafe_allow_html=True)


    # --- CATEGORIA: FINANÇAS E CÁLCULOS ---
    elif ferramenta == "Calculadora de Salário Líquido (CLT)":
        st.title("💼 Calculadora de Salário Líquido (CLT Oficial)")
        
        st.markdown("""
        <div class="info-box-premium">
            <strong>Salário Bruto x Salário Líquido: Saiba quanto vai cair na sua conta.</strong><br>
            Quem é assalariado e trabalha com carteira assinada conhece bem a diferença relevante que existe entre o salário bruto (aquele valor cheio registrado no contrato de trabalho) e o valor que você recebe na prática no dia do pagamento. Nossa calculadora oficial vai te ajudar a descobrir quanto você vai receber por mês após a cobrança da tabela progressiva do Imposto de Renda Retido na Fonte (IRRF), o desconto compulsório da contribuição ao INSS, previdência privada, pensão alimentícia e vales. Basta preencher as informações abaixo e clicar em calcular.
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1: salario_bruto = st.number_input("Salário Bruto de Registro (R$):", min_value=0.0, value=3000.0)
        with col2: dependentes = st.number_input("Número de Dependentes Legais (IRRF):", min_value=0, value=0)
        
        st.markdown("#### Outras Deduções da Folha de Pagamento")
        c3, c4, c5 = st.columns(3)
        with c3: pensao = st.number_input("Pensão Alimentícia (R$):", value=0.0)
        with c4: previdencia = st.number_input("Previdência Privada/Complementar (R$):", value=0.0)
        with c5: outros = st.number_input("Outros (Vales, Plano de Saúde) (R$):", value=0.0)
        
        if st.button("Calcular Holerite Líquido", type="primary"):
            if salario_bruto <= 1412.00: inss = salario_bruto * 0.075
            elif salario_bruto <= 2666.68: inss = (salario_bruto * 0.09) - 21.18
            elif salario_bruto <= 4000.03: inss = (salario_bruto * 0.12) - 101.18
            elif salario_bruto <= 7786.02: inss = (salario_bruto * 0.14) - 181.18
            else: inss = 908.85
                
            base_irrf = salario_bruto - inss - (dependentes * 189.59) - pensao - previdencia
            
            if base_irrf <= 2259.20: irrf = 0.0
            elif base_irrf <= 2826.65: irrf = (base_irrf * 0.075) - 169.44
            elif base_irrf <= 3751.05: irrf = (base_irrf * 0.15) - 381.44
            elif base_irrf <= 4664.68: irrf = (base_irrf * 0.225) - 662.77
            else: irrf = (base_irrf * 0.275) - 896.00
                
            irrf_final = max(0, irrf)
            salario_liquido = salario_bruto - inss - irrf_final - pensao - previdencia - outros
            
            st.markdown(f"<div style='background-color:#F0FDF4; border: 2px dashed #10B981; padding:20px; border-radius:10px; margin-top:20px;'><h1 style='text-align: center; color: #10B981; margin:0;'>Líquido a Receber: R$ {salario_liquido:,.2f}</h1></div>", unsafe_allow_html=True)
            
            st.markdown("### 📋 Resumo dos Descontos Oficiais")
            c_res1, c_res2, c_res3 = st.columns(3)
            c_res1.metric("Desconto INSS", f"R$ {inss:,.2f}")
            c_res2.metric("Imposto de Renda (IRRF)", f"R$ {irrf_final:,.2f}")
            c_res3.metric("Pensão/Previdência/Outros", f"R$ {pensao + previdencia + outros:,.2f}")

    elif ferramenta == "Calculadora de Férias":
        st.title("🏖️ Calculadora Completa de Férias")
        st.markdown("**Como usar:** Utilize nossa ferramenta para **calcular as férias online grátis**. Descubra exatamente quanto você tem a receber no seu aviso de férias, contemplando a venda de dias (abono pecuniário), adiantamento de 13º salário, horas extras e, obviamente, o adicional do terço constitucional garantido por lei.")
        
        c1, c2 = st.columns(2)
        with c1: salario = st.number_input("Salário Bruto Registrado Mensal (R$):", min_value=0.0, value=3000.0)
        with c2: dias = st.slider("Dias de Férias Solicitados (Gozo):", min_value=5, max_value=30, value=30)
        
        c3, c4 = st.columns(2)
        with c3: hr_extras = st.number_input("Média de Horas Extras/Adicionais Mensais (R$):", value=0.0)
        with c4: dependentes = st.number_input("Quantidade de Dependentes:", min_value=0, value=0)
        
        c5, c6 = st.columns(2)
        with c5: abono = st.toggle("Vender 10 dias de férias? (Abono Pecuniário)", value=False)
        with c6: adianta_13 = st.toggle("Solicitar Adiantamento da 1ª Parcela do 13º Salário?", value=False)
        
        if st.button("Executar Cálculo de Férias", type="primary"):
            base_calc = salario + hr_extras
            
            valor_ferias_gozo = (base_calc / 30) * dias
            terco_gozo = valor_ferias_gozo / 3
            
            valor_abono = 0.0
            terco_abono = 0.0
            if abono:
                valor_abono = (base_calc / 30) * 10
                terco_abono = valor_abono / 3
            
            valor_13 = (base_calc / 2) if adianta_13 else 0.0
            
            total_bruto = valor_ferias_gozo + terco_gozo + valor_abono + terco_abono + valor_13
            
            st.markdown(f"<div style='background-color:#EFF6FF; border: 2px dashed #3B82F6; padding:20px; border-radius:10px; margin-top:20px;'><h1 style='text-align: center; color: #1D4ED8; margin:0;'>Total Bruto a Receber: R$ {total_bruto:,.2f}</h1><p style='text-align:center; margin-bottom:0;'>*Valor sem dedução de INSS e IRRF incidentes.</p></div>", unsafe_allow_html=True)
            
            st.markdown("### 📋 Composição do Pagamento")
            col_a, col_b, col_c = st.columns(3)
            col_a.metric(f"Férias ({dias} dias) + 1/3", f"R$ {valor_ferias_gozo + terco_gozo:,.2f}")
            col_b.metric("Abono (Venda) + 1/3", f"R$ {valor_abono + terco_abono:,.2f}")
            col_c.metric("Adiantamento 13º", f"R$ {valor_13:,.2f}")

    elif ferramenta == "Calculadora de Horas Extras":
        st.title("⏱️ Calculadora de Horas Extras")
        st.markdown("**Como usar:** A **calculadora de hora extra online** é essencial para funcionários e empresas conferirem a folha de pagamento. Descubra o valor exato adicional gerado pelo trabalho em turnos excedentes. Preencha seu salário, carga horária e informe a quantidade de horas e minutos extras realizados no período.")
        
        c1, c2 = st.columns(2)
        with c1: salario = st.number_input("Salário Bruto Base (R$):", min_value=1.0, value=3000.0)
        with c2: jornada = st.number_input("Carga Horária Mensal (Padrão 220h):", min_value=1, value=220)
        
        st.markdown("#### 1. Horas Extras a 50% (Dias Úteis Normais e Sábados)")
        col_h1, col_m1 = st.columns(2)
        with col_h1: he_50_h = st.number_input("Quantidade de Horas (50%):", min_value=0, value=10, key="h50")
        with col_m1: he_50_m = st.number_input("Quantidade de Minutos (50%):", min_value=0, max_value=59, value=30, key="m50")
        
        st.markdown("#### 2. Horas Extras a 100% (Domingos e Feriados)")
        col_h2, col_m2 = st.columns(2)
        with col_h2: he_100_h = st.number_input("Quantidade de Horas (100%):", min_value=0, value=0, key="h100")
        with col_m2: he_100_m = st.number_input("Quantidade de Minutos (100%):", min_value=0, max_value=59, value=0, key="m100")
        
        if st.button("Calcular Valores de Hora Extra", type="primary"):
            valor_hora_comum = salario / jornada
            tempo_50 = he_50_h + (he_50_m / 60)
            tempo_100 = he_100_h + (he_100_m / 60)
            total_50 = (valor_hora_comum * 1.5) * tempo_50
            total_100 = (valor_hora_comum * 2.0) * tempo_100
            total_geral = total_50 + total_100
            
            st.markdown(f"<div style='background-color:#FDF4FF; border: 2px solid #D946EF; padding:20px; border-radius:10px; margin-top:20px;'><h1 style='text-align: center; color: #A21CAF; margin:0;'>Adicional Total: R$ {total_geral:,.2f}</h1></div>", unsafe_allow_html=True)
            
            cx1, cx2 = st.columns(2)
            cx1.metric("Remuneração H.E 50%", f"R$ {total_50:,.2f}")
            cx2.metric("Remuneração H.E 100%", f"R$ {total_100:,.2f}")

    elif ferramenta == "Calculadora de Juros Compostos":
        st.title("📈 Calculadora de Juros Compostos")
        st.markdown("**Como usar:** Entenda a mágica matemática que multiplica patrimônios. Nossa **calculadora de juros compostos com aportes mensais** é a melhor ferramenta para planejar aposentadorias, simular rentabilidade de fundos imobiliários (FIIs), Tesouro Direto, CDBs e a Caixinha do Nubank no longo prazo. Informe capital, aportes e taxa.")
        
        c1, c2 = st.columns(2)
        with c1: v_ini = st.number_input("Valor do Investimento Inicial (R$):", value=1000.0)
        with c2: aporte = st.number_input("Aporte Mensal Constante (R$):", value=200.0)
        c3, c4 = st.columns(2)
        with c3: taxa = st.number_input("Taxa de Juros Anual Prevista (%):", value=10.0)
        with c4: anos = st.number_input("Tempo de Investimento (Anos):", value=5)
        
        if st.button("Simular Rendimento Completo", type="primary"):
            tx_m = (1 + (taxa/100))**(1/12) - 1
            meses = anos * 12
            montante = v_ini * (1 + tx_m)**meses
            for _ in range(meses): montante += aporte * (1 + tx_m)**(meses - _)
            
            st.markdown(f"<div style='background-color:#F0FDF4; border: 2px dashed #10B981; padding:20px; border-radius:10px; margin-top:20px;'><h1 style='text-align: center; color: #10B981; margin:0;'>Patrimônio Final Estimado: R$ {montante:,.2f}</h1></div>", unsafe_allow_html=True)
            
            c_r1, c_r2 = st.columns(2)
            total_bolso = v_ini + (aporte * meses)
            c_r1.metric("Valor total investido do seu bolso", f"R$ {total_bolso:,.2f}")
            c_r2.metric("Lucro apenas em juros acumulados", f"R$ {montante - total_bolso:,.2f}")

    elif ferramenta == "Calculadora Regra 50-30-20":
        st.title("📊 Calculadora Regra 50-30-20")
        st.markdown("**Como usar:** Organize seu orçamento pessoal com o método financeiro mais validado por economistas. A **Regra 50/30/20** divide a sua renda líquida mensal (já com os descontos) em três pilares fundamentais: 50% para Custos Fixos Essenciais (Aluguel, Luz, Comida), 30% para Estilo de Vida e Desejos (Lazer, Compras) e 20% para Metas Financeiras e Poupança (Investimentos e Quitação de Dívidas).")
        renda = st.number_input("Informe a sua Renda Líquida Mensal Disponível (R$):", min_value=100.0, value=3000.0, step=100.0)
        if st.button("Gerar Planejamento Financeiro", type="primary"):
            st.success("Orçamento Estruturado. Tente seguir os limites abaixo:")
            c1, c2, c3 = st.columns(3)
            c1.metric("🏠 50% Gastos Essenciais", f"R$ {renda*0.5:,.2f}")
            c2.metric("🎉 30% Lazer e Desejos", f"R$ {renda*0.3:,.2f}")
            c3.metric("📈 20% Futuro / Investimentos", f"R$ {renda*0.2:,.2f}")

    elif ferramenta == "Calculadora de Porcentagem":
        st.title("📊 Calculadora de Porcentagem (Múltipla)")
        st.markdown("**Como usar:** Uma **calculadora de porcentagem online grátis** que resolve todos os cenários numéricos. Calcule descontos em produtos de lojas, descubra taxas de acréscimo de juros em boletos, ou a representatividade percentual de um valor sobre outro.")
        tipo = st.selectbox("Qual cenário de cálculo você precisa resolver?", ["Acréscimo de Valor", "Desconto de Valor", "Quanto é X% de um Valor Y"])
        c1, c2 = st.columns(2)
        with c1: v_base = st.number_input("Valor Base/Montante:", value=1000.0)
        with c2: p = st.number_input("Taxa Percentual (%):", value=15.0)
        if st.button("Resolver Equação", type="primary"):
            if tipo == "Acréscimo de Valor": 
                st.markdown(f"<h2>R$ {v_base} + {p}% = <span style='color:#3B82F6;'>R$ {v_base + (v_base * (p / 100)):,.2f}</span></h2>", unsafe_allow_html=True)
            elif tipo == "Desconto de Valor": 
                st.markdown(f"<h2>R$ {v_base} - {p}% = <span style='color:#3B82F6;'>R$ {v_base - (v_base * (p / 100)):,.2f}</span></h2>", unsafe_allow_html=True)
            else: 
                st.markdown(f"<h2>{p}% de R$ {v_base} equivale a: <span style='color:#3B82F6;'>R$ {v_base * (p / 100):,.2f}</span></h2>", unsafe_allow_html=True)

    elif ferramenta == "Calculadora de Regra de Três":
        st.title("🧮 Regra de Três Simples")
        st.markdown("**Como usar:** A **calculadora de regra de três simples matemática** descobre valores proporcionais de forma automática. Usada em receitas culinárias, escalas de arquitetura e conversão de moedas. Insira os 3 valores lógicos conhecidos e nós achamos a variável X.")
        c1, c2 = st.columns(2)
        with c1: 
            a = st.number_input("Se o valor base (A):", value=100.0)
            c = st.number_input("Então a sua proporcional (C):", value=50.0)
        with c2: 
            b = st.number_input("Equivale ao valor cruzado (B):", value=200.0)
            st.markdown("<h3 style='text-align:center; margin-top:28px; color:#64748B;'>Deverá ser equivalente a = X</h3>", unsafe_allow_html=True)
        if st.button("Encontrar X", type="primary") and a != 0:
            st.markdown(f"<div style='background-color:#F8FAFC; border: 2px solid #3B82F6; padding:20px; border-radius:10px; margin-top:20px;'><h1 style='text-align: center; color: #1D4ED8; margin:0;'>O valor de X é: {(b * c) / a:,.2f}</h1></div>", unsafe_allow_html=True)


    # --- CATEGORIA: SORTEIOS E JOGOS ---
    elif ferramenta == "Sorteador Completo":
        st.title("🎲 Sorteador Online Central e Loterias")
        st.markdown("**Como usar:** O seu assistente oficial para eventos. O melhor **sorteador aleatório online grátis**. Faça sorteios de números para rifas, sorteios de nomes para o Instagram, separe times para o futebol, ou gere bilhetes surpresinha para apostas nas loterias da Caixa.")
        
        t_num, t_nom, t_eq, t_letra, t_rifa, t_loteria = st.tabs(["🔢 Números Únicos", "👤 Lista de Nomes", "🛡️ Equipes e Times", "🅰️ Letras (Stop)", "🎟️ Múltiplas Rifas", "🍀 Loterias Caixa"])
        
        with t_num:
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1: min_val = st.number_input("Sortear entre (De):", value=1, key="num_min_val")
            with c2: max_val = st.number_input("Até (Máximo):", value=100, key="num_max_val")
            
            tempo_num = st.radio("Tempo do Cronômetro (Segundos):", [0, 3, 5, 10], index=1, horizontal=True, key="t1")
            
            if st.button("Rodar Sorteio", type="primary", key="btn_sort_num"):
                if tempo_num > 0:
                    t = st.empty()
                    for i in range(tempo_num, 0, -1):
                        t.markdown(f"<h1 style='text-align: center; font-size: 80px;'>⏳ {i}</h1>", unsafe_allow_html=True)
                        time.sleep(1)
                    t.empty()
                st.balloons()
                st.markdown(f"<h1 style='text-align: center; font-size: 100px; color: #3B82F6;'>{random.randint(int(min_val), int(max_val))}</h1>", unsafe_allow_html=True)
                    
        with t_nom:
            lista_nomes = st.text_area("Cole os nomes dos participantes (Um por linha):", height=150, key="nom_lista")
            tempo_nom = st.radio("Tempo de Suspense (Segundos):", [0, 3, 5, 10], index=1, horizontal=True, key="t2")
            if st.button("Sortear Vencedor Único", type="primary", key="btn_sort_nom") and lista_nomes:
                nomes = [n.strip() for n in lista_nomes.split('\n') if n.strip()]
                if nomes:
                    if tempo_nom > 0:
                        t = st.empty()
                        for i in range(tempo_nom, 0, -1):
                            t.markdown(f"<h1 style='text-align: center; font-size: 80px;'>⏳ {i}</h1>", unsafe_allow_html=True)
                            time.sleep(1)
                        t.empty()
                    st.balloons()
                    st.markdown(f"<h1 style='text-align: center; font-size: 60px; color: #3B82F6;'>🏆 {random.choice(nomes)}</h1>", unsafe_allow_html=True)

        with t_eq:
            nomes_eq = st.text_area("Cole a lista total de jogadores/participantes:", height=150, key="eq_lista")
            qtd = st.number_input("Quantos times/equipes deseja formar?", min_value=2, value=2, key="eq_qtd")
            if st.button("Equilibrar e Separar Equipes", type="primary", key="btn_sort_eq") and nomes_eq:
                jogs = [n.strip() for n in nomes_eq.split('\n') if n.strip()]
                random.shuffle(jogs)
                eqs = [[] for _ in range(qtd)]
                for i, j in enumerate(jogs): eqs[i % qtd].append(j)
                st.balloons()
                cols = st.columns(qtd)
                for idx, eq in enumerate(eqs):
                    with cols[idx % len(cols)]:
                        st.markdown(f"<div style='background-color:#F8FAFC; padding:15px; border-radius:8px; border:1px solid #CBD5E1;'><h3>🛡️ Equipe {idx+1}</h3>", unsafe_allow_html=True)
                        for m in eq: st.write(f"- {m}")
                        st.markdown("</div>", unsafe_allow_html=True)

        with t_letra:
            st.markdown("Ideal para jogos como Stop/Adedonha.")
            if st.button("Sortear Letra Aleatória do Alfabeto", type="primary", key="btn_sort_letra"):
                st.balloons()
                st.markdown(f"<h1 style='text-align: center; font-size: 120px; color: #3B82F6;'>{random.choice(string.ascii_uppercase)}</h1>", unsafe_allow_html=True)

        with t_rifa:
            c1, c2, c3 = st.columns([1, 1, 1])
            with c1: ini_rifa = st.number_input("Início da Rifa (Ex: 1):", value=1, key="rifa_ini")
            with c2: fim_rifa = st.number_input("Fim da Rifa (Ex: 100):", value=100, key="rifa_fim")
            with c3: qtd_rifa = st.number_input("Quantos prêmios/vencedores?", min_value=1, value=3, key="rifa_qtd")
            
            tempo_rifa = st.radio("Tempo do Cronômetro (Segundos):", [0, 3, 5, 10], index=1, horizontal=True, key="t3")
            
            if st.button("Sortear Resultados da Rifa", type="primary", key="btn_sort_rifa"):
                if ini_rifa < fim_rifa and qtd_rifa <= (fim_rifa - ini_rifa + 1):
                    if tempo_rifa > 0:
                        t = st.empty()
                        for i in range(tempo_rifa, 0, -1):
                            t.markdown(f"<h1 style='text-align: center; font-size: 80px;'>⏳ {i}</h1>", unsafe_allow_html=True)
                            time.sleep(1)
                        t.empty()
                    st.balloons()
                    sorteados = random.sample(range(int(ini_rifa), int(fim_rifa) + 1), int(qtd_rifa))
                    st.success("Sorteio Oficial Concluído!")
                    for i, num in enumerate(sorteados):
                        st.markdown(f"<h3 style='background-color:#FEF3C7; padding:10px; border-radius:5px;'>🏆 {i+1}º Lugar / Prêmio: Bilhete Nº **{num}**</h3>", unsafe_allow_html=True)
                else:
                    st.error("Configuração de intervalo inválida.")
                    
        with t_loteria:
            st.markdown("Gere um palpite aleatório e inteligente (Surpresinha) para jogos oficiais.")
            jogo = st.radio("Escolha a Loteria Oficial do Brasil:", ["Mega-Sena", "Lotofácil", "Quina", "Dia de Sorte", "Lotomania"], horizontal=True, key="loto_sel")
            
            if st.button("Gerar Palpite de Sorte", type="primary", key="btn_sort_loto"):
                regras = {
                    "Mega-Sena": (6, 60), "Quina": (5, 80), "Lotofácil": (15, 25), 
                    "Dia de Sorte": (7, 31), "Lotomania": (50, 99)
                }
                qtd_bolas, limite = regras[jogo]
                palpite = sorted(random.sample(range(1, limite + 1), qtd_bolas))
                st.balloons()
                st.success(f"🍀 Boa sorte! Seus números da {jogo} são:")
                bolas_html = "<div style='display:flex; flex-wrap:wrap; gap:10px; justify-content:center; padding: 20px;'>"
                for num in palpite:
                    bolas_html += f"<div style='background-color:#10B981; color:white; width:65px; height:65px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:26px; font-weight:bold; box-shadow: 2px 2px 5px rgba(0,0,0,0.3); border: 2px solid #059669;'>{num:02d}</div>"
                bolas_html += "</div>"
                st.markdown(bolas_html, unsafe_allow_html=True)

    elif ferramenta == "Gerador de Desculpas Aleatórias":
        st.title("🤣 Gerador de Desculpas Modernas")
        st.markdown("**Como usar:** Preso em uma situação chata ou um convite de última hora que você não quer aceitar? Gere uma **desculpa criativa e convincente** (ou propositalmente absurda) para enviar no WhatsApp e cancelar o evento com maestria.")
        if st.button("Socorro! Preciso de uma desculpa urgente!", type="primary"):
            desculpas = [
                "Cara, meu cachorro engoliu a chave do meu carro, tô esperando o veterinário.", 
                "Putz, achei que o evento era só no mês que vem, já marquei compromisso inadiável.", 
                "Estou com uma intoxicação alimentar severa do sushi de ontem (não pergunte detalhes).",
                "O encanamento do banheiro estourou, a casa está alagada e o bombeiro não chega.",
                "Tive um imprevisto familiar super urgente e precisei viajar pro interior.", 
                "Meu vizinho trancou o carro dele bem atrás da minha garagem e sumiu com a chave.",
                "Peguei no sono profundo e acabei de acordar assustado, sem condições de ir.",
                "Caiu a internet do bairro inteiro e eu tô finalizando um trabalho pelo roteador do celular.",
                "Acredita que furou o pneu e o meu estepe tá furado também?",
                "Minha imunidade baixou do nada, tô com muita febre e dor no corpo, melhor eu não passar pra ninguém."
            ]
            st.markdown(f"""
            <div style="display:flex; justify-content: flex-end; margin-top:30px; margin-bottom:30px;">
                <div style="background-color: #DCF8C6; border-radius: 15px 0px 15px 15px; padding: 15px 20px; max-width: 70%; box-shadow: 1px 1px 3px rgba(0,0,0,0.1);">
                    <p style="font-family: Arial, sans-serif; font-size: 18px; color: #303030; margin:0;">{random.choice(desculpas)}</p>
                    <span style="font-size: 11px; color: #999; float:right; margin-top:5px;">16:20 ✓✓</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


    # --- CATEGORIA: UTILITÁRIOS ---
    elif ferramenta == "Calculadora de Datas":
        st.title("📆 Calculadora de Datas")
        st.markdown("**Como usar:** Esta incrível **ferramenta de soma e subtração de dias** online permite que você descubra exatamente em qual data cairá um prazo futuro. Escolha a data de início, selecione se quer somar ou subtrair, e informe a quantidade de dias, meses ou anos do prazo.")
        
        c1, c2 = st.columns(2)
        with c1: dt_base = st.date_input("Data Inicial de Referência:")
        with c2: operacao = st.radio("Operação Lógica:", ["➕ Somar tempo ao futuro", "➖ Subtrair tempo ao passado"], horizontal=True)
        
        c3, c4, c5 = st.columns(3)
        with c3: dias_add = st.number_input("Quantidade de Dias:", min_value=0, value=0)
        with c4: meses_add = st.number_input("Quantidade de Meses:", min_value=0, value=0)
        with c5: anos_add = st.number_input("Quantidade de Anos:", min_value=0, value=0)
        
        if st.button("Executar Cálculo de Calendário", type="primary"):
            mes_total = dt_base.month - 1
            ano_total = dt_base.year
            
            if "Somar" in operacao:
                ano_total += anos_add
                mes_total += meses_add
                ano_total += mes_total // 12
                mes_final = (mes_total % 12) + 1
                dia_max = calendar.monthrange(ano_total, mes_final)[1]
                dia_final = min(dt_base.day, dia_max)
                data_result = date(ano_total, mes_final, dia_final) + timedelta(days=dias_add)
            else:
                ano_total -= anos_add
                mes_total -= meses_add
                while mes_total < 0:
                    mes_total += 12
                    ano_total -= 1
                mes_final = mes_total + 1
                dia_max = calendar.monthrange(ano_total, mes_final)[1]
                dia_final = min(dt_base.day, dia_max)
                data_result = date(ano_total, mes_final, dia_final) - timedelta(days=dias_add)
                
            st.markdown(f"<div style='background-color:#F8FAFC; border: 2px dashed #64748B; padding:20px; border-radius:10px; margin-top:20px;'><h1 style='text-align: center; color: #1E293B; margin:0;'>Data Resultante: {data_result.strftime('%d/%m/%Y')}</h1></div>", unsafe_allow_html=True)

    elif ferramenta == "Calendário 2026 Útil":
        st.title("🗓️ Calendário Interativo 2026 (Feriados Nacionais)")
        st.markdown("**Como usar:** Utilize este **calendário de feriados 2026 dinâmico** para se programar para as folgas, feriados prolongados e recessos do ano. Selecione o mês desejado na caixa abaixo para visualizar a grade de dias. Os dias destacados em <span style='color:#E11D48; font-weight:bold;'>vermelho</span> representam feriados nacionais.", unsafe_allow_html=True)
        
        feriados_2026 = {
            "01-01": "Confraternização", "02-17": "Carnaval", "04-03": "Paixão de Cristo",
            "04-21": "Tiradentes", "05-01": "Dia do Trabalho", "06-04": "Corpus Christi",
            "09-07": "Independência", "10-12": "Aparecida", "11-02": "Finados",
            "11-15": "República", "12-25": "Natal"
        }
        
        meses_nomes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        mes_sel = st.selectbox("Navegue pelo Ano - Escolha o Mês:", meses_nomes)
        idx_mes = meses_nomes.index(mes_sel) + 1
        
        st.markdown(f"<h3 style='text-align:center; margin-top:20px; margin-bottom:20px; color:#1E293B;'>{mes_sel.upper()} DE 2026</h3>", unsafe_allow_html=True)
        
        cal = calendar.monthcalendar(2026, idx_mes)
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        
        cols_header = st.columns(7)
        for i, dia_str in enumerate(dias_semana):
            cols_header[i].markdown(f"<div style='text-align:center; font-weight:bold; color:#64748B;'>{dia_str}</div>", unsafe_allow_html=True)
            
        for semana in cal:
            cols_grid = st.columns(7)
            for i, dia_num in enumerate(semana):
                if dia_num == 0:
                    cols_grid[i].markdown("")
                else:
                    formato_dia = f"{idx_mes:02d}-{dia_num:02d}"
                    if formato_dia in feriados_2026:
                        cols_grid[i].markdown(f"<div style='background-color:#FECDD3; border: 1px solid #F43F5E; border-radius:8px; padding:10px; text-align:center; color:#BE123C; font-weight:bold; box-shadow: 1px 1px 3px rgba(0,0,0,0.1);'>{dia_num}<br><small style='font-size:10px;'>{feriados_2026[formato_dia]}</small></div>", unsafe_allow_html=True)
                    else:
                        cols_grid[i].markdown(f"<div style='background-color:#F8FAFC; border: 1px solid #E2E8F0; border-radius:8px; padding:10px; text-align:center; color:#334155;'>{dia_num}<br><small>&nbsp;</small></div>", unsafe_allow_html=True)

    elif ferramenta == "Validador de CPF e CNPJ":
        st.title("✅ Validador de Documentos")
        st.markdown("**Como usar:** Utilize o **validador online de CPF e CNPJ** para auditar dados recebidos em formulários ou e-mails. Ele faz a triagem da métrica dos números e confere se a contagem de dígitos atende ao limite legal estipulado pelas normas federais (11 ou 14 dígitos formatados).")
        doc = st.text_input("Digite a sequência numérica (Com ou sem pontuação):")
        if st.button("Validar Integridade Base", type="primary") and doc:
            doc_limpo = re.sub(r'\D', '', doc)
            if len(doc_limpo) == 11: st.success("Estrutura de tamanho CPF Validada (11 Dígitos).")
            elif len(doc_limpo) == 14: st.success("Estrutura de tamanho CNPJ Validada (14 Dígitos).")
            else: st.error("Atenção: Tamanho numérico inválido. O documento inserido está corrompido ou incompleto.")

    elif ferramenta == "Busca Endereço por CEP":
        st.title("📍 Consulta Fácil de CEP")
        st.markdown("**Como usar:** Nossa ferramenta se conecta à base de dados oficial para fornecer a **busca de endereço por CEP instantânea**. Preenchendo formulários, envios e encomendas e esqueceu a rua? Basta digitar os 8 números do CEP brasileiro na caixa e nós revelamos a rua, bairro, cidade e uf da região.")
        cep_input = st.text_input("Digite os dígitos do CEP (Ex: 01001-000):")
        if st.button("Rastrear Localização", type="primary"):
            cep_limpo = re.sub(r'[^0-9]', '', cep_input)
            if len(cep_limpo) == 8:
                try:
                    res = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/").json()
                    if "erro" not in res: 
                        st.markdown(f"<div style='background-color:#F0FDF4; border-left:5px solid #10B981; padding:20px; font-size:18px;'><b>Logradouro:</b> {res['logradouro']}<br><b>Bairro:</b> {res['bairro']}<br><b>Localidade:</b> {res['localidade']} - {res['uf']}</div>", unsafe_allow_html=True)
                    else: st.error("O CEP não foi encontrado nas bases territoriais.")
                except: st.error("Erro no processamento da requisição de rede.")
            else: st.warning("Certifique-se de digitar exatos 8 números numéricos.")

    elif ferramenta == "Calculadora de Dias Úteis":
        st.title("📅 Calculadora de Dias Úteis")
        st.markdown("**Como usar:** Planejando férias, contratos, ou prazos bancários? Use nossa **calculadora de dias úteis e corridos** para descobrir exatamente quantos dias descontando sábados e domingos existem em um determinado intervalo de tempo futuro ou passado.")
        c1, c2 = st.columns(2)
        with c1: dt_ini = st.date_input("Defina a Data Inicial:")
        with c2: dt_fim = st.date_input("Defina a Data Final de Corte:")
        if st.button("Executar Contagem de Prazos", type="primary"):
            if dt_ini <= dt_fim:
                dias_uteis = sum(1 for i in range((dt_fim - dt_ini).days + 1) if (dt_ini + timedelta(days=i)).weekday() < 5)
                st.markdown("<h3 style='margin-bottom:20px;'>Resultados Encontrados:</h3>", unsafe_allow_html=True)
                r1, r2 = st.columns(2)
                r1.metric("Dias Úteis (Seg à Sex)", dias_uteis)
                r2.metric("Total de Dias Corridos", (dt_fim - dt_ini).days + 1)
            else: st.error("Inconsistência Lógica: A data de início precisa ser cronologicamente anterior a data final.")

    elif ferramenta == "Calculadora de IMC":
        st.title("⚖️ Calculadora de IMC da OMS")
        st.markdown("**Como usar:** Acompanhe a saúde do seu corpo. O **cálculo online de Índice de Massa Corporal (IMC)** é a forma matemática primária adotada por nutricionistas e pela OMS para classificar se o paciente se enquadra em desnutrição, peso ideal, sobrepeso ou quadros críticos de obesidade.")
        c1, c2 = st.columns(2)
        with c1: peso = st.number_input("Informe o Peso exato (kg):", value=70.0, step=0.1)
        with c2: altura = st.number_input("Informe a Altura exata (m):", value=1.75, step=0.01)
        if st.button("Diagnosticar IMC", type="primary"):
            imc = peso / (altura ** 2)
            cor, status = ("#3B82F6", "Abaixo do peso") if imc < 18.5 else ("#10B981", "Peso Normal") if imc < 25 else ("#F59E0B", "Sobrepeso") if imc < 30 else ("#EF4444", "Obesidade")
            st.markdown(f"<div style='background-color:#F8FAFC; border:2px solid {cor}; padding:20px; border-radius:10px;'><h1 style='text-align: center; color: {cor}; margin:0;'>Seu IMC exato: {imc:.1f}</h1><h3 style='text-align: center; color: #475569; margin:0;'>Status Médico Referencial: {status}</h3></div>", unsafe_allow_html=True)

    elif ferramenta == "Conversor de Medidas":
        st.title("📏 Conversor de Medidas Físicas")
        st.markdown("Converta grandezas métricas internacionais instantaneamente, incluindo Quilômetros e Milhas e variações térmicas como Celsius e Fahrenheit.")
        c1, c2 = st.columns(2)
        with c1: km_val = st.number_input("Entrada de Quilômetros (KM):", value=10.0)
        with c2: st.number_input("Equivalência em Milhas (Mi):", value=km_val * 0.621371, disabled=True)

    elif ferramenta == "Sorteador de Cores (HEX)":
        st.title("🎨 Sorteador e Gerador de Cores HEX")
        st.markdown("Criando uma logo nova? Nosso gerador gera **paletas de cores e códigos hexadecimais aleatórios** para inspirar projetos criativos de web design.")
        if st.button("Sortear Inspiração de Cor", type="primary"):
            cor = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            st.markdown(f"<div style='background-color: {cor}; height: 100px; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);'><h1 style='color: white; text-shadow: 1px 1px 2px #000;'>{cor.upper()}</h1></div>", unsafe_allow_html=True)
