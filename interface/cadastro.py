# Arquivo: cadastro.py
# Classe de cadastro do aplicativo 

# Bibliotecas e Módulos
from interface import Base
import tkinter as tk
from tkinter import messagebox, ttk, Toplevel, Frame, Label, Button
from pacotes import database
from pacotes.database import registrar_novo_usuario, adicionar_chave_pix
from pacotes.utils import hash_senha, mask_cpf, gerar_comprovante
from .pagina_base import Base
import sqlite3

class Cadastro(Base):
    """
    Página de cadastro do aplicativo.
    """
    def setup_widgets(self):

        tk.Label(self, text="Cadastro", font=("Arial", 20), bg="black", fg="red").pack(pady=(40,15))
        campos = ["CPF (só números)", "Nome Completo", "Email", "Senha"]
        self.entradas = {}

        for campo in campos:
            tk.Label(self, text=f"{campo}:", bg="black", fg="white", font=("Arial", 10)).pack()
            entry = tk.Entry(self, show="*" if campo == "Senha" else None, width=30)
            entry.pack(pady=3)
            self.entradas[campo.split(' ')[0].lower()] = entry

        tk.Button(self, text="Registrar", command=self.registrar, bg="red", fg="white").pack(pady=10)
        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PaginaInicial"), bg="grey", fg="white").pack()

    def registrar(self):
        """
        Registra um novo usuário.
        """
        dados = {campo: entry.get() for campo, entry in self.entradas.items()}
        
        if not all(dados.values()):
            """        
            Verifica se todos os campos foram preenchidos.
            """
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return
        
        cpf = dados['cpf']

        if not cpf.isdigit() or len(cpf) != 11: 
            """
            Verifica se o CPF tem o formato válido, ou seja, possui apenas números e 11 dígitos.
            """
            messagebox.showerror("Erro de Cadastro", "CPF inválido. Digite apenas 11 números.")
            return

        email = dados['email']
        dominios_validos = ["@gmail.com", "@hotmail.com", "@yahoo.com", "@outlook.com", "@live.com"]

        if "@" not in email or not any(email.endswith(dominio) for dominio in dominios_validos):
            """
            Verifica se o e-mail contém um dos domínios válidos.
            """
            messagebox.showerror("Erro de Cadastro", "Formato de e-mail inválido ou domínio não suportado.")
            return

        senha = dados['senha']
        
        if len(senha) < 6:
            """
            Verifica se a senha no mínimo 6 caracteres.
            """
            messagebox.showerror("Erro de Cadastro", "A senha deve ter no mínimo 6 caracteres.")
            return

        try:
            """
            Adiciona o novo usuário no banco de dados.
            """
            database.registrar_novo_usuario(dados['cpf'], dados['nome'], dados['email'], hash_senha(dados['senha']))
            database.adicionar_chave_pix(dados['cpf'], 'CPF', dados['cpf'])
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            self.controller.show_frame("Login")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF ou Email já cadastrado.")
