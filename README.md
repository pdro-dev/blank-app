---

# 📌 **Sistema de Registros com Streamlit**  

Este é um sistema web desenvolvido com **Streamlit**, utilizando **SQLite** para armazenamento de dados. O sistema permite **cadastro, consulta, exportação de registros e geração de PDFs**.

---

## 🚀 **Funcionalidades**  
✅ **Login e Autenticação** - Controle de acesso ao sistema  
✅ **Cadastro de Registros** - Adicione novos registros com **Nome, Email e Descrição**  
✅ **Consulta de Registros** - Visualize os registros em uma tabela interativa  
✅ **Exportação de Dados** - Exporte os registros para **CSV** e **Excel (.xlsx)**  
✅ **Geração de PDF** - Exporte documentos individuais no formato PDF  
✅ **Remoção de Registros** - Exclua registros diretamente pela interface  
✅ **Interface Responsiva** - Design adaptável para diferentes tamanhos de tela  

---

## 🛠 **Instalação e Configuração**  

### 🔹 **1. Clone o Repositório**  
```sh
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 🔹 **2. Crie um Ambiente Virtual (Opcional)**
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### 🔹 **3. Instale as Dependências**
```sh
pip install -r requirements.txt
```

### 🔹 **4. Execute a Aplicação**
```sh
streamlit run streamlit_app.py
```

---

## 📂 **Estrutura do Projeto**
```
📦 seu-projeto
│── 📄 streamlit_app.py      # Código principal do Streamlit
│── 📄 requirements.txt      # Lista de dependências
│── 📄 README.md             # Documentação do projeto
│── 📂 database.db           # Banco de dados SQLite (gerado automaticamente)
```

---

## 📜 **Como Usar**
### **🔐 Login**
- Acesse com **Usuário:** `admin` e **Senha:** `1234` (Pode ser modificado no código) (código modificado para login direto)

### **📋 Cadastro de Registros**
- Preencha os campos **Nome, Email e Descrição**
- Clique em **Salvar** para adicionar um novo registro

### **📊 Consulta e Exportação**
- Veja todos os registros cadastrados  
- Exporte os registros para **CSV** ou **Excel**  
- Expanda um registro para mais detalhes  

### **📄 Geração de Documento**
- Selecione um registro na aba **"Visualização"**  
- Clique em **"Baixar PDF"** para exportar o documento  

---

## 🛠 **Tecnologias Utilizadas**
- **Python 3.11+**  
- **Streamlit** (Interface Web)  
- **SQLite** (Banco de Dados)  
- **Pandas** (Manipulação de Dados)  
- **ReportLab** (Geração de PDFs)  
- **OpenPyXL** (Exportação para Excel)  

---

## 📝 **To-Do e Melhorias Futuras**
✅ Melhorar layout da tabela de registros  
✅ Implementar tema escuro automático  
⬜ Criar novos níveis de usuários (admin, editor, visitante)  
⬜ Adicionar busca avançada nos registros  

---

## 🧑‍💻 **Contribuição**
Contribuições são bem-vindas! Para sugerir melhorias:
1. Faça um **fork** do repositório  
2. Crie uma **nova branch** (`feature-nova-funcionalidade`)  
3. Faça as alterações e **commit** (`git commit -m "Adicionando nova funcionalidade"`)  
4. Envie um **pull request** 🚀  

---

## 📞 **Contato**
Caso tenha dúvidas ou sugestões, entre em contato:
📧 **Email:** [seuemail@example.com](mailto:seuemail@example.com)  
🔗 **LinkedIn:** [linkedin.com/in/seu-perfil](https://linkedin.com/in/seu-perfil)  

---

Agora seu projeto tem uma **documentação completa e profissional**! 🚀🔥  
Se precisar de ajustes ou quiser adicionar mais informações, me avise. 😊
