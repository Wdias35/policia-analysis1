import fitz  # PyMuPDF

def extrair_dados_pdf(arquivo_pdf):
    doc = fitz.open(stream=arquivo_pdf.read(), filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto
