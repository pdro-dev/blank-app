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

# Função para detectar o modo do usuário via JavaScript
def detect_theme():
    st.markdown(
        """
        <script>
        function sendThemeToStreamlit() {
            var theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
            window.parent.postMessage({theme: theme}, '*');
        }
        sendThemeToStreamlit();
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', sendThemeToStreamlit);
        </script>
        <div id="theme-detect"></div>
        """,
        unsafe_allow_html=True
    )

    # Captura a mensagem do tema e armazena no session_state
    theme = st.session_state.get("theme", "light")  # Padrão: Light Mode
    return theme

# Página de Login Simples
def login_page():
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

# Página de Consulta de Registros
def consulta_registros():
    st.title("📋 Consulta de Registros")
    conn = get_db_connection()
    registros = conn.execute("SELECT * FROM registros").fetchall()
    
    if registros:
        for r in registros:
            with st.expander(f"📌 {r[1]} ({r[2]})"):
                st.write(f"**Descrição:** {r[3]}")
                col1, col2 = st.columns([4, 1])
                with col2:
                    if st.button("🗑️ Excluir", key=f"delete_{r[0]}"):
                        conn.execute("DELETE FROM registros WHERE id = ?", (r[0],))
                        conn.commit()
                        conn.close()
                        st.success("✅ Registro excluído com sucesso!")
                        st.rerun()
        conn.close()
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

    # Detecta o tema do usuário
    theme = detect_theme()

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
        if theme == "dark":
            # 🎨 Modo Escuro (Dark Mode)
            markdown_content = f"""
            <div style="
                border: 2px solid rgba(255, 255, 255, 0.2); 
                border-radius: 10px; 
                padding: 20px; 
                background-color: rgba(50, 50, 50, 0.8);
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
                color: #E0E0E0;
            ">
                <h2 style="text-align: center; color: #F9F9F9;">📌 Documento Oficial</h2>
                <hr style="border-top: 1px solid rgba(255, 255, 255, 0.3);">
                <p><strong style="color: #FF8C00;">🆔 ID:</strong> {registro[0]}</p>
                <p><strong style="color: #87CEFA;">👤 Nome:</strong> {registro[1]}</p>
                <p><strong style="color: #98FB98;">📧 Email:</strong> {registro[2]}</p>
                <p><strong style="color: #FFD700;">📝 Descrição:</strong></p>
                <div style="
                    border-left: 5px solid #FFD700; 
                    padding: 10px;
                    background-color: rgba(80, 80, 80, 0.8);
                    font-style: normal;
                    color: #FFFFFF;
                ">
                    {registro[3]}
                </div>
                <hr style="border-top: 1px solid rgba(255, 255, 255, 0.3);">
                <p style="text-align: right; font-size: 12px; color: #AAAAAA;">📅 Data de emissão: {st.session_state.get('data_atual', 'N/A')}</p>
            </div>
            """
        else:
            # 🌞 Modo Claro (Light Mode)
            markdown_content = f"""
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
                <p><strong style="color: #FF4500;">🆔 ID:</strong> {registro[0]}</p>
                <p><strong style="color: #1E90FF;">👤 Nome:</strong> {registro[1]}</p>
                <p><strong style="color: #008000;">📧 Email:</strong> {registro[2]}</p>
                <p><strong style="color: #DAA520;">📝 Descrição:</strong></p>
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
            """

        # Renderiza o documento formatado conforme o tema
        st.markdown(markdown_content, unsafe_allow_html=True)
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
