import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 📌 Função para carregar arquivos CSV com tratamento de erro
def carregar_csv(nome_arquivo):
    if os.path.exists(nome_arquivo):
        return pd.read_csv(nome_arquivo)
    else:
        st.error(f"⚠️ O arquivo `{nome_arquivo}` não foi encontrado. Envie-o para o GitHub!")
        return None  # Retorna None para evitar erro

# 📌 Função para calcular a porcentagem de votos em cada bairro
def calcular_percentual(df, coluna_votos):
    if df is None:
        return None
    total_votos = df[coluna_votos].sum()
    df['% VOTOS'] = (df[coluna_votos] / total_votos) * 100
    return df

# 📍 Carregar e processar os dados de Pedro Porto
df_pedro = carregar_csv('Relatório_de_votos_com_coordenadas.csv')
if df_pedro is not None:
    df_pedro = df_pedro.groupby('BAIRRO', as_index=False).agg({
        'PEDRO PORTO 2024 1T': 'sum',
        'LATITUDE': 'mean',
        'LONGITUDE': 'mean'
    })
    df_pedro = calcular_percentual(df_pedro, 'PEDRO PORTO 2024 1T')

# 📍 Carregar e processar os dados de Martha Rocha
df_martha = carregar_csv('martha_rocha_com_coordenadas.csv')
if df_martha is not None:
    df_martha = calcular_percentual(df_martha, 'Votos Absolutos')

# 📍 Carregar e processar os dados de Ciro Gomes
df_ciro = carregar_csv('ciro_com_coordenadas.csv')
if df_ciro is not None:
    df_ciro = calcular_percentual(df_ciro, 'Votos Absolutos')

# ⚠️ Se algum arquivo estiver ausente, interrompe o app
if df_pedro is None or df_martha is None or df_ciro is None:
    st.stop()

# 🔹 Criar os gráficos
fig_pedro = px.scatter_mapbox(
    df_pedro,
    lat='LATITUDE',
    lon='LONGITUDE',
    hover_name='BAIRRO',
    hover_data={'PEDRO PORTO 2024 1T': True, '% VOTOS': True},
    size='% VOTOS',
    size_max=50,
    color_discrete_sequence=['green'],
    title="Mapa de votação Pedro Porto"
)

fig_martha = px.scatter_mapbox(
    df_martha,
    lat='LATITUDE',
    lon='LONGITUDE',
    hover_name='Bairro',
    hover_data={'Votos Absolutos': True, '% VOTOS': True},
    size='% VOTOS',
    size_max=50,
    color_discrete_sequence=['blue'],
    title="Mapa de votação Martha Rocha"
)

fig_ciro = px.scatter_mapbox(
    df_ciro,
    lat='LATITUDE',
    lon='LONGITUDE',
    hover_name='Bairro',
    hover_data={'Votos Absolutos': True, '% VOTOS': True},
    size='% VOTOS',
    size_max=50,
    color_discrete_sequence=['red'],
    title="Mapa de votação Ciro Gomes"
)

# Configuração do layout do mapa
for fig in [fig_pedro, fig_martha, fig_ciro]:
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=10,
        mapbox_center={"lat": -22.9068, "lon": -43.1729},
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

# 🔹 Layout do Streamlit
st.title('Mapas de votação ajustados para proporção de votos')

# Dropdown para selecionar o mapa desejado
opcao_mapa = st.selectbox(
    "Escolha um mapa para visualizar",
    ["Pedro Porto", "Martha Rocha", "Ciro Gomes"]
)

# Exibir o mapa escolhido
if opcao_mapa == "Pedro Porto":
    st.plotly_chart(fig_pedro)
elif opcao_mapa == "Martha Rocha":
    st.plotly_chart(fig_martha)
elif opcao_mapa == "Ciro Gomes":
    st.plotly_chart(fig_ciro)
