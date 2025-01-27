import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import  os


# Configuração da página para ocupar toda a largura
st.set_page_config(layout="wide")

# Título do Dashboard
st.title("Dashboard Trafego Pago")

# Caminho do Arquivo Excel
caminho_arquivo = os.getenv('DATABASE_URL')

# Ler o arquivo Excel
try:
    df = pd.read_excel(caminho_arquivo, engine="openpyxl")
    st.write("✅ Ola seja bem vindo")
except FileNotFoundError:
    st.error("❌ Arquivo não encontrado. Verifique o caminho.")
    st.stop()
except Exception as e:
    st.error(f"❌ Erro ao carregar o arquivo: {e}")
    st.stop()

# Remover espaços extras nos nomes das colunas
df.columns = df.columns.str.strip()

# Filtro para selecionar campanha
campanhas = df["nome_campanha"].unique()
campanha_selecionada = st.selectbox("Selecione a Campanha", campanhas)

# Filtrar os dados pela campanha selecionada
df_filtrado = df[df["nome_campanha"] == campanha_selecionada]



# Botão para redefinir o filtro
if st.button("Redefinir Filtro"):
    # Limpar a seleção do filtro (no caso da campanha)
    if 'campanha_selecionada' in st.session_state:
        del st.session_state['campanha_selecionada']
    st.rerun()  # Redefine a página para recarregar os filtros



# Calcular os KPIs
impressões_total = df_filtrado["impressões"].sum()
cliques_total = df_filtrado["cliques"].sum()
ctr_total = (cliques_total / impressões_total) * 100 if impressões_total > 0 else 0
investimento_total = df_filtrado["investimento"].sum()
cpc_total = investimento_total / cliques_total if cliques_total > 0 else 0
cpm_total = (investimento_total / impressões_total * 1000) if impressões_total > 0 else 0


# Título da seção
st.markdown("##  Métricas Meta Ads")

# Título da seção
# Criar colunas para exibição alinhada lado a lado
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(label="Impressões", value=f"{impressões_total:,.0f}")

with col2:
    st.metric(label="Cliques", value=f"{cliques_total:,.0f}")

with col3:
    st.metric(label="CTR", value=f"{ctr_total:.2f}%")

with col4:
    st.metric(label="Investimento", value=f"R$ {investimento_total:,.2f}")

with col5:
    st.metric(label="CPC", value=f"R$ {cpc_total:,.2f}")

with col6:
    st.metric(label="CPM", value=f"R$ {cpm_total:,.2f}")



# Supondo que seu DataFrame já esteja carregado
# df = pd.read_csv("seuarquivo.csv")

# Renomeando as colunas para consistência
df.columns = df.columns.str.strip().str.lower()  
df = df.rename(columns={'nome_criativos': 'criativos', 'investimento': 'investimento', 'impressões': 'impressoes'})

# Transformando os dados para formato longo (melt)
df_melted = df.melt(id_vars=['criativos'], value_vars=['investimento', 'impressoes'], var_name='métrica', value_name='valor')

# Criando o gráfico com barras agrupadas horizontais no mesmo eixo
grafico = alt.Chart(df_melted).mark_bar(size=20).encode(  # Reduzindo a largura das barras
    x='valor:Q',  # Eixo X representa os valores (Investimento e Impressões)
    y=alt.Y('criativos:N', title='Criativos', sort='-x'),  # Criativos no eixo Y
    color='métrica:N',  # Cor diferenciada para Investimento e Impressões
    tooltip=['criativos', 'métrica', 'valor']  # Exibindo detalhes ao passar o mouse
).properties(
    title="Criativo com maior Investimento e Impressões",
    width=400,  # Largura ajustada para o gráfico ficar menor
    height=300  # Altura ajustada
)



# Caminho do Arquivo Excel
caminho_arquivo = os.getenv('DATABASE_URL')


# Limpar espaços extras nos nomes das colunas
df.columns = df.columns.str.strip()

# Definir as colunas que você quer analisar
metricas = ['salvaram', 'compartilharam', 'comentaram']

# Verificar se as colunas existem no DataFrame
for metrica in metricas:
    if metrica not in df.columns:
        st.error(f"Coluna '{metrica}' não encontrada no DataFrame!")
        st.stop()

# Somar os valores das colunas definidas
df_soma = df[metricas].sum().reset_index()
df_soma.columns = ['Métrica', 'Valor']

# Ordenar os valores do menor para o maior
df_soma = df_soma.sort_values('Valor', ascending=True)

# Criar gráfico de **colunas empilhadas na vertical** com barras mais finas
chart = alt.Chart(df_soma).mark_bar(size=50).encode(  # Reduzindo a largura das barras
    x=alt.X('Métrica:N', sort='-y', title='Métricas'),
    y=alt.Y('Valor:Q', title='Quantidade', stack='zero'),
    color=alt.Color('Métrica:N', legend=alt.Legend(title="Ações")),
).properties(
    title='Gráfico de Colunas Empilhadas: Salvar, Compartilhar, Comentar',
    width=400,  # Largura ajustada para o gráfico ficar menor
    height=300  # Altura ajustada
)



# Organizar os gráficos lado a lado usando beta_columns
col1, col2, = st.columns(2)

# Exibir gráficos lado a lado
with col1:
    st.altair_chart(grafico, use_container_width=True)

with col2:
    st.altair_chart(chart, use_container_width=True)



