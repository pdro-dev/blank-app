import streamlit as st
import sqlite3
import pandas as pd
import os
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import textwrap

# Configuração da página
st.set_page_config(page_title="Sistema de Registros", layout="wide")

# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.execute(
        """CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            descricao TEXT
        )"""
    )
    return conn

# Função para exportar os registros como CSV
def exportar_csv():
    conn = get_db_connection()
    registros = conn.execute("SELECT * FROM registros").fetchall()
    conn.close()

    if not registros:
        st.warning("Nenhum dado para exportar.")
        return None

    df = pd.DataFrame(registros, columns=["ID", "Nome", "Email", "Descrição"])
    csv_file = "registros_exportados.csv"
    df.to_csv(csv_file, index=False, encoding="utf-8")

    # Criar link de download
    with open(csv_file, "rb") as file:
        b64 = base64.b64encode(file.read()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{csv_file}">📥 Baixar CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

# Função para exportar os registros como Excel
def exportar_xlsx():
    conn = get_db_connection()
    registros = conn.execute("SELECT * FROM registros").fetchall()
    conn.close()

    if not registros:
        st.warning("Nenhum dado para exportar.")
        return None

    df = pd.DataFrame(registros, columns=["ID", "Nome", "Email", "Descrição"])
    xlsx_file = "registros_exportados.xlsx"

    # Salvar em formato Excel
    df.to_excel(xlsx_file, index=False, engine="openpyxl")

    # Criar link de download
    with open(xlsx_file, "rb") as file:
        b64 = base64.b64encode(file.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{xlsx_file}">📥 Baixar Excel</a>'
    st.markdown(href, unsafe_allow_html=True)

# Página de Consulta de Registros com Exportação
def consulta_registros():
    st.title("📋 Consulta de Registros")
    conn = get_db_connection()
    registros = conn.execute("SELECT * FROM registros").fetchall()
    conn.close()

    if registros:
        df = pd.DataFrame(registros, columns=["ID", "Nome", "Email", "Descrição"])
        st.table(df)

        if st.button("📤 Exportar para CSV"):
            exportar_csv()

        if st.button("📤 Exportar para Excel"):
            exportar_xlsx()
        
        for r in registros:
            with st.expander(f"📌 {r[1]} ({r[2]})"):
                st.write(f"**Descrição:** {r[3]}")
                col1, col2 = st.columns([4, 1])
                with col2:
                    if st.button("🗑️ Excluir", key=f"delete_{r[0]}"):
                        conn = get_db_connection()
                        conn.execute("DELETE FROM registros WHERE id = ?", (r[0],))
                        conn.commit()
                        conn.close()
                        st.success("✅ Registro excluído com sucesso!")
                        st.rerun()
    else:
        st.info("Nenhum registro encontrado.")

def gerar_pdf(registro):
    pdf_file = f"documento_{registro[0]}.pdf"
    
    # Criar um PDF usando o ReportLab
    c = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4
    margem_esquerda = 50
    margem_superior = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(margem_esquerda, margem_superior, "📌 Documento Oficial")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margem_esquerda, margem_superior - 40, f"🆔 ID: {registro[0]}")
    c.drawString(margem_esquerda, margem_superior - 60, f"👤 Nome: {registro[1]}")
    c.drawString(margem_esquerda, margem_superior - 80, f"📧 Email: {registro[2]}")

    # Configurar título da descrição
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margem_esquerda, margem_superior - 110, "📝 Descrição:")

    # Ajuste para a descrição multi-linha
    descricao = registro[3]
    c.setFont("Helvetica", 12)

    # Envolver texto para respeitar a largura da página
    wrapped_text = textwrap.wrap(descricao, width=100)  # Ajusta o tamanho da linha

    y_position = margem_superior - 130
    for line in wrapped_text:
        c.drawString(margem_esquerda, y_position, line)
        y_position -= 15  # Move para a próxima linha

    c.showPage()
    c.save()

    # Criar link para download do PDF
    with open(pdf_file, "rb") as file:
        b64 = base64.b64encode(file.read()).decode()
    
    href = f'<a href="data:application/pdf;base64,{b64}" download="{pdf_file}">📥 Baixar PDF</a>'
    return href

# Página de Visualização de Documento com Exportação para PDF
def visualizar_documento():
    st.title("📄 Visualização de Documento")

    conn = get_db_connection()
    registros = conn.execute("SELECT * FROM registros").fetchall()
    conn.close()

    if not registros:
        st.info("Nenhum registro disponível para visualização.")
        return

    ids = [r[0] for r in registros]
    selected_id = st.selectbox("Selecione um registro", ids)

    registro = next((r for r in registros if r[0] == selected_id), None)
    if registro:
        st.markdown(f"""
            <h2 style="text-align: center;">📌 Documento Oficial</h2>
            <p><strong>🆔 ID:</strong> {registro[0]}</p>
            <p><strong>👤 Nome:</strong> {registro[1]}</p>
            <p><strong>📧 Email:</strong> {registro[2]}</p>
            <p><strong>📝 Descrição:</strong> {registro[3]}</p>
        """, unsafe_allow_html=True)

        # Gerar e exibir botão para download do PDF
        pdf_download_link = gerar_pdf(registro)
        st.markdown(pdf_download_link, unsafe_allow_html=True)
    else:
        st.error("Registro não encontrado.")

# Adicionar autenticação
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 Login")
    user = st.text_input("Usuário", key="user")
    password = st.text_input("Senha", type="password", key="password")

    if st.button("Entrar"):
        if user == "" and password == "":
            st.session_state["authenticated"] = True
            st.success("✅ Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("❌ Usuário ou senha incorretos.")
else:
    menu = st.sidebar.radio("📌 Menu", ["Consulta", "Cadastro", "Visualização", "Logout"])

    if menu == "Consulta":
        consulta_registros()
    elif menu == "Cadastro":
        st.title("📝 Cadastro de Novo Registro")
        nome = st.text_input("Nome Completo")
        email = st.text_input("Email")
        descricao = st.text_area("Descrição")

        if st.button("Salvar"):
            conn = get_db_connection()
            conn.execute("INSERT INTO registros (nome, email, descricao) VALUES (?, ?, ?)", (nome, email, descricao))
            conn.commit()
            conn.close()
            st.success("✅ Registro salvo com sucesso!")
            st.rerun()
    elif menu == "Visualização":
        visualizar_documento()
    elif menu == "Logout":
        st.session_state["authenticated"] = False
        st.rerun()
