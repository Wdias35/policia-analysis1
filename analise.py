import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

def gerar_tabela(lista_de_textos):
    dados = []

    for texto in lista_de_textos:
        tipo = extrair_info(texto, "Tipo de ocorrência:")
        endereco = extrair_info(texto, "Endereço:")
        bairro = extrair_info(texto, "Bairro:")
        horario = extrair_info(texto, "Horário:")

        dados.append({
            "Tipo": tipo,
            "Endereço": endereco,
            "Bairro": bairro,
            "Horário": horario
        })

    return pd.DataFrame(dados)

def extrair_info(texto, chave):
    for linha in texto.split('\n'):
        if chave in linha:
            return linha.replace(chave, '').strip()
    return "Não informado"

def gerar_graficos(df):
    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(df, x="Bairro", title="Ocorrências por Bairro")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(df, names="Tipo", title="Tipos de Ocorrência")
        st.plotly_chart(fig, use_container_width=True)

def gerar_mapa(df):
    mapa = folium.Map(location=[-23.5, -46.6], zoom_start=11)

    for i, row in df.iterrows():
        folium.Marker(
            location=geolocalizar(row["Endereço"] + ", " + row["Bairro"]),
            popup=f'{row["Tipo"]} às {row["Horário"]}',
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(mapa)

    folium_static(mapa)

def geolocalizar(endereco):
    # Simulação – substituir por geolocalização real (Google Maps API, etc.)
    # Você pode usar APIs como OpenCage, Here ou Nominatim
    return [-23.5, -46.6]
