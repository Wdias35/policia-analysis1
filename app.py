import streamlit as st
from leitor_pdf import extrair_dados_pdf
from analise import gerar_tabela, gerar_graficos, gerar_mapa

st.set_page_config(page_title="Sistema de Análise Criminal", layout="wide")
st.title("📊 Boas-vindas ao Sistema de Análise Criminal")

uploaded_files = st.file_uploader("📂 Enviar PDFs de ocorrências policiais", type="pdf", accept_multiple_files=True)

if uploaded_files:
    dados_extraidos = []

    for file in uploaded_files:
        texto = extrair_dados_pdf(file)
        dados_extraidos.append(texto)

    df = gerar_tabela(dados_extraidos)

    st.subheader("📋 Ocorrências Detectadas")
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Gráficos de Análise")
    gerar_graficos(df)

    st.subheader("🗺️ Mapa das Ocorrências")
    gerar_mapa(df)
