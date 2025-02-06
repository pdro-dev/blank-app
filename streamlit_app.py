import streamlit as st
import sqlite3
import pandas as pd
import os
try:
    from fpdf import FPDF
except ModuleNotFoundError:
    os.system("pip install fpdf")
    from fpdf import FPDF
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

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

# Definir o caminho para a fonte
FONT_PATH = "DejaVuSans.ttf"

class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "", 16)  # Fonte adicionada corretamente
        self.cell(200, 10, "Documento Oficial", ln=True, align="C")
        self.ln(10)

def gerar_pdf(registro):
    pdf_file = f"documento_{registro[0]}.pdf"
    
    # Criar um PDF usando o ReportLab
    c = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica", 16)
    c.drawString(50, height - 50, "📌 Documento Oficial")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"🆔 ID: {registro[0]}")
    c.drawString(50, height - 120, f"👤 Nome: {registro[1]}")
    c.drawString(50, height - 140, f"📧 Email: {registro[2]}")

    # Ajuste para a descrição multi-linha
    descricao = f"📝 Descrição:\n{registro[3]}"
    text = c.beginText(50, height - 180)
    text.setFont("Helvetica", 12)
    text.textLines(descricao)

    c.drawText(text)
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
        st.markdown(
            f"""
            <div style="
                border: 2px solid #ddd; 
                border-radius: 10px; 
                padding: 20px; 
                background-color: #ffffff;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                color: #333;
            ">
                <h2 style="text-align: center; color: #333;">📌 Documento Oficial</h2>
                <hr>
                <p><strong>🆔 ID:</strong> {registro[0]}</p>
                <p><strong>👤 Nome:</strong> {registro[1]}</p>
                <p><strong>📧 Email:</strong> {registro[2]}</p>
                <p><strong>📝 Descrição:</strong></p>
                <div style="
                    border-left: 5px solid #DAA520; 
                    padding: 10px;
                    background-color: #f0f4ff;
                    font-style: normal;
                    color: #333;
                ">
                    {registro[3]}
                </div>
                <hr>
                <p style="text-align: right; font-size: 12px; color: #666;">📅 Data de emissão: {st.session_state.get('data_atual', 'N/A')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Gerar e exibir botão para download do PDF
        pdf_download_link = gerar_pdf(registro)
        st.markdown(pdf_download_link, unsafe_allow_html=True)
    else:
        st.error("Registro não encontrado.")

# Layout do Menu Lateral
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
            if nome and email and descricao:
                conn = get_db_connection()
                conn.execute("INSERT INTO registros (nome, email, descricao) VALUES (?, ?, ?)", (nome, email, descricao))
                conn.commit()
                conn.close()
                st.success("✅ Registro salvo com sucesso!")
                st.rerun()
            else:
                st.error("❌ Todos os campos são obrigatórios.")
    elif menu == "Visualização":
        visualizar_documento()
    elif menu == "Logout":
        st.session_state["authenticated"] = False
        st.rerun()
