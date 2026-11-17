import streamlit as st
from datetime import datetime
from google import genai
from google.genai import types

# Configuração da página
st.set_page_config(page_title="ProCoach AI - Tênis & Personal", page_icon="🎾", layout="wide")

# Barra lateral para configuração da Chave de API e Navegação
with st.sidebar:
    st.header("⚙️ Configurações")
    api_key = st.text_input("Gemini API Key",value=st.secrets.get("GEMINI_API_KEY", ""), type="password")
    st.info("Insira sua chave do Google AI Studio para ativar a IA.")
    
    st.markdown("---")
    st.header("📌 Módulos do Sistema")
    modulo = st.radio("Escolha a ferramenta:", ["🎾 Treino de Tênis", "💪 Personal Training"])

# Título principal dinâmico
st.title(f"ProCoach AI — Módulo: {modulo}")
st.markdown("Gerador inteligente de periodização, horários e prescrição de treinos.")

# Pegando data e hora atual no fuso do Brasil
data_atual = datetime.now().strftime("%d/%m/%Y")
hora_atual = datetime.now().strftime("%H:%M")

# ==========================================
# MÓDULO 1: TREINO DE TÊNIS
# ==========================================
if modulo == "🎾 Treino de Tênis":
    st.markdown("### Planejamento de Sessão em Quadra")
    
    with st.form("form_tenis"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome_aluno_t = st.text_input("Nome do Aluno/Atleta", placeholder="Ex: Carlos Alberto")
            nivel_t = st.select_slider("Nível Técnico", options=["Iniciante", "Intermediário", "Avançado", "Competitivo"], key="niv_t")
            tipo_quadra = st.selectbox("Tipo de Quadra", ["Saibro (Clay)", "Dura (Hard Court)", "Grama (Grass)", "Beach Tennis / Indoor"])
            
        with col2:
            duracao_t = st.number_input("Duração da Aula (minutos)", min_value=30, max_value=180, value=60, step=15, key="dur_t")
            foco_t = st.text_input("Foco Principal do Treino", placeholder="Ex: Correção de forehand, consistência no fundo, saque e voleio")
            
        obs_t = st.text_area("Observações ou Dificuldades Recorrentes", placeholder="Ex: O aluno está abrindo muito o cotovelo no backhand...", key="obs_t")
        
        submit_t = st.form_submit_button("Gerar Treino de Tênis Completo")

    if submit_t:
        if not api_key:
            st.error("Insira sua API Key na barra lateral.")
        elif not nome_aluno_t or not foco_t:
            st.warning("Preencha o Nome e o Foco Principal.")
        else:
            with st.spinner("Construindo sessão de treinamento e buscando referências visuais..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    sys_prompt_tenis = f"""
                    Você é um Treinador de Tênis profissional de alto rendimento.
                    Sua tarefa é criar um plano de aula prático, dinâmico e estruturado.
                    
                    INFORMAÇÕES DE REGISTRO:
                    - Data de emissão: {data_atual}
                    - Horário de emissão: {hora_atual}
                    
                    REGRA OBRIGATÓRIA PARA VÍDEOS:
                    Para cada drill ou exercício principal indicado, adicione obrigatoriamente um link de pesquisa do YouTube formatado em Markdown (exemplo: [🎥 Ver execução no YouTube](https://www.youtube.com/results?search_query=como+fazer+drill+de+tenis)). O link deve ser uma busca direcionada no YouTube para o exercício específico.
                    
                    O plano deve conter:
                    1. Cabeçalho formatado com Data e Hora.
                    2. Aquecimento e Ativação.
                    3. Drills Técnicos / Sitacionais (com o link de vídeo em cada um).
                    4. Situação de Jogo / Pontuação.
                    5. Volta à Calma.
                    """
                    
                    user_prompt_tenis = f"""
                    Crie um treino de tênis para:
                    - Aluno: {nome_aluno_t}
                    - Nível: {nivel_t}
                    - Superfície: {tipo_quadra}
                    - Duração: {duracao_t} minutos
                    - Foco: {foco_t}
                    - Observações: {obs_t if obs_t else 'Nenhuma'}
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.5-flash-lite',
                        contents=user_prompt_tenis,
                        config=types.GenerateContentConfig(system_instruction=sys_prompt_tenis, temperature=0.4)
                    )
                    
                    st.success("Treino de Tênis gerado com sucesso!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                    st.download_button("📥 Baixar Treino (.txt)", response.text, file_name=f"tenis_{nome_aluno_t.lower().replace(' ', '_')}_{data_atual.replace('/', '-')}.txt")
                except Exception as e:
                    st.error(f"Erro: {e}")

# ==========================================
# MÓDULO 2: PERSONAL TRAINING
# ==========================================
elif modulo == "💪 Personal Training":
    st.markdown("### Planejamento de Musculação e Preparação Física")
    
    with st.form("form_personal"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome_aluno_p = st.text_input("Nome do Aluno", placeholder="Ex: Mariana Souza")
            objetivo_p = st.selectbox("Objetivo Principal", ["Hipertrofia", "Emagrecimento / Definição", "Força Máxima", "Resistência / Funcional", "Prevenção de Lesões / Core"])
            experiencia_p = st.selectbox("Nível de Treinamento", ["Iniciante (Pouca experiência)", "Intermediário (Treina regularmente)", "Avançado"])
            
        with col2:
            duracao_p = st.number_input("Tempo de Treino (minutos)", min_value=30, max_value=120, value=60, step=15, key="dur_p")
            local_p = st.selectbox("Local de Treino", ["Academia Completa", "Treino em Casa / Condomínio (Pesos livres/Elásticos)", "Peso Corporal (Calistenia)"])
            
        lesoes_p = st.text_area("Lesões, Restrições ou Dores Articulares", placeholder="Ex: Condromalácia patelar leve...", key="les_p")
        
        submit_p = st.form_submit_button("Gerar Ficha de Personal Completa")

    if submit_p:
        if not api_key:
            st.error("Insira sua API Key na barra lateral.")
        elif not nome_aluno_p:
            st.warning("Preencha o Nome do Aluno.")
        else:
            with st.spinner("Montando periodização e links de execução..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    sys_prompt_personal = f"""
                    Você é um Professor de Educação Física especialista em musculação e biomecânica.
                    
                    INFORMAÇÕES DE REGISTRO:
                    - Data de emissão: {data_atual}
                    - Horário de emissão: {hora_atual}
                    
                    REGRA OBRIGATÓRIA PARA VÍDEOS:
                    Para cada exercício da ficha, adicione obrigatoriamente um link de pesquisa em formato Markdown apontando para o YouTube (ex: [🎥 Ver execução correta](https://www.youtube.com/results?search_query=como+executar+o+exercicio+corretamente)). Substitua o nome do exercício na query.
                    
                    O treino deve conter:
                    1. Cabeçalho formatado com Data e Hora.
                    2. Aquecimento específico / Ativação.
                    3. Parte Principal (Exercício, Séries, Repetições, Descanso e o link de vídeo).
                    4. Cuidados com as restrições informadas.
                    5. Volta à calma.
                    """
                    
                    user_prompt_personal = f"""
                    Crie uma ficha de treino de musculação/preparação física para:
                    - Aluno: {nome_aluno_p}
                    - Objetivo: {objetivo_p}
                    - Experiência: {experiencia_p}
                    - Duração: {duracao_p} minutos
                    - Local: {local_p}
                    - Restrições/Lesões: {lesoes_p if lesoes_p else 'Nenhuma restrição relatada'}
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.5-flash-lite',
                        contents=user_prompt_personal,
                        config=types.GenerateContentConfig(system_instruction=sys_prompt_personal, temperature=0.3)
                    )
                    
                    st.success("Ficha de Personal gerada com sucesso!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                    st.download_button("📥 Baixar Ficha (.txt)", response.text, file_name=f"personal_{nome_aluno_p.lower().replace(' ', '_')}_{data_atual.replace('/', '-')}.txt")
                except Exception as e:
                    st.error(f"Erro: {e}")