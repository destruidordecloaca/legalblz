import sqlite3
import streamlit as st
import pandas as pd

# Função para criar a tabela
def criar_tabela():
    conn = sqlite3.connect("funcionarios.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cargo TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Função para inserir funcionário
def inserir_funcionario(nome, cargo, email):
    conn = sqlite3.connect("funcionarios.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO funcionarios (nome, cargo, email) VALUES (?, ?, ?)", (nome, cargo, email))
    conn.commit()
    conn.close()

# Função para listar funcionários
def listar_funcionarios():
    conn = sqlite3.connect("funcionarios.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM funcionarios")
    funcionarios = cursor.fetchall()
    conn.close()
    return funcionarios

# Inicializa a tabela
criar_tabela()

# Configuração da página
st.set_page_config(page_title="Cadastro de Funcionários", page_icon=":guardsman:")
st.header("Cadastro de Funcionários")

# Formulário de cadastro
with st.form(key="form_funcionario", clear_on_submit=True):
    st.warning("Preencha todos os campos!")
    nome = st.text_input("Nome")
    cargo = st.text_input("Cargo")
    email = st.text_input("Email")
    botao_submit = st.form_submit_button("Adicionar")

    if botao_submit:
        if nome and cargo and email:
            inserir_funcionario(nome, cargo, email)
            st.success("Funcionário adicionado com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos.")

# Exibição da lista de funcionários
st.subheader("Lista de Funcionários")
dados = listar_funcionarios()
if dados:
    df = pd.DataFrame(dados, columns=["ID", "Nome", "Cargo", "Email"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("Nenhum funcionário cadastrado ainda.")
