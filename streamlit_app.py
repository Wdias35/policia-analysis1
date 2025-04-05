import streamlit as st

import streamlit as st
import pandas as pd
import re
from PyPDF2 import PdfReader
from geopy.geocoders import Nominatim
from sklearn.cluster import KMeans
import folium
from streamlit_folium import folium_static

# Configuração do Streamlit
st.set_page_config(page_title="Análise Policial", layout="wide")

# Funções de Processamento
def extract_pdf_data(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = "".join([page.extract_text() for page in reader.pages])
    
    # Regex para extração de dados (ajuste conforme seu modelo de PDF)
    patterns = {
        'data': r'Data:\s*(\d{2}/\d{2}/\d{4})',
        'hora': r'Hora:\s*(\d{2}:\d{2})',
        'endereco': r'Endereço:\s*(.*?)(?=\n)',
        'natureza': r'Natureza:\s*(.*?)(?=\n)'
    }
    
    return {key: re.search(pattern, text).group(1) if re.search(pattern, text) else None 
            for key, pattern in patterns.items()}

def geocode_address(address):
    geolocator = Nominatim(user_agent="police_app")
    try:
        location = geolocator.geocode(address + ", Brasil")
        return (location.latitude, location.longitude) if location else (None, None)
    except:
        return (None, None)

# Interface
st.title("🚨 Sistema de Otimização Policial")
uploaded_files = st.file_uploader("Envie os PDFs de ocorrências", type="pdf", accept_multiple_files=True)

if uploaded_files:
    # Processamento dos dados
    dados = [extract_pdf_data(pdf) for pdf in uploaded_files]
    df = pd.DataFrame(dados).dropna()
    
    # Geocodificação
    df[['lat', 'lon']] = df['endereco'].apply(
        lambda x: pd.Series(geocode_address(x))
    )
    
    # Clusterização
    kmeans = KMeans(n_clusters=3)
    df['cluster'] = kmeans.fit_predict(df[['lat', 'lon']])
    
    # Mapa
    st.header("Mapa de Hotspots")
    m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=12)
    for idx, row in df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=5,
            color='red',
            fill=True
        ).add_to(m)
    
    folium_static(m, width=1200)
    
    # Sugestões
    st.subheader("Locais Prioritários para Viaturas")
    for center in kmeans.cluster_centers_:
        st.write(f"📍 Coordenadas: ({center[0]:.4f}, {center[1]:.4f})")
    
    # Estatísticas
    st.subheader("📊 Insights:")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Ocorrências", len(df))
        st.metric("Horário de Pico", df['hora'].mode()[0])
    with col2:
        st.metric("Área Mais Crítica", df['endereco'].mode()[0])
        st.metric("Natureza Principal", df['natureza'].mode()[0])
