import streamlit as st
import sqlite3

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

# Página de Login Simples
def login_page():
    st.title("🔐 Login")
    user = st.text_input("Usuário", key="user")
    password = st.text_input("Senha", type="password", key="password")
    
    if st.button("Entrar"):
        if user == "admin" and password == "1234":
            st.session_state["authenticated"] = True
            st.success("✅ Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("❌ Usuário ou senha incorretos.")

# Página de Consulta de Registros
def consulta_registros():
    st.title("📋 Consulta de Registros")
    conn = get_db_connection()
    registros = conn.execute("SELECT * FROM registros").fetchall()
    conn.close()

    if registros:
        st.write("Registros encontrados:")
        st.table([{"ID": r[0], "Nome": r[1], "Email": r[2], "Descrição": r[3]} for r in registros])
    else:
        st.info("Nenhum registro encontrado.")

# Página de Cadastro de Formulários
def cadastro_formulario():
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

# Página de Visualização de Documento
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
        ---
        ### 📌 Documento Oficial  
        **Nome:** {registro[1]}  
        **Email:** {registro[2]}  
        **Descrição:**  
        {registro[3]}  
        ---
        """)
    else:
        st.error("Registro não encontrado.")

# Layout do Menu Lateral
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_page()
else:
    menu = st.sidebar.radio("📌 Menu", ["Consulta", "Cadastro", "Visualização", "Logout"])

    if menu == "Consulta":
        consulta_registros()
    elif menu == "Cadastro":
        cadastro_formulario()
    elif menu == "Visualização":
        visualizar_documento()
    elif menu == "Logout":
        st.session_state["authenticated"] = False
        st.rerun()
