# Arquivo: login.py
# Classe de login do aplicativo

# Bibliotecas e Módulos
import tkinter as tk
from tkinter import messagebox
from pacotes import database
from pacotes.utils import hash_senha
from .pagina_base import Base 

class Login(Base):
    """
    Página de login do aplicativo.
    """
    def setup_widgets(self):
        """
        Configura os widgets da página de login.
        """
        tk.Label(self, text="Login", font=("Arial", 20), bg="black", fg="red").pack(pady=(40,15))

        tk.Label(self, text="CPF:", bg="black", fg="white").pack()
        self.cpf_entry = tk.Entry(self, width=30)
        self.cpf_entry.pack()

        tk.Label(self, text="Senha:", bg="black", fg="white").pack()
        self.senha_entry = tk.Entry(self, show="*", width=30)
        self.senha_entry.pack()

        tk.Button(self, text="Entrar", command=self.autenticar, bg="red", fg="white").pack(pady=10)
        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PaginaInicial"), bg="grey", fg="white").pack(pady=(20,0))
    
    def autenticar(self):
        """
        Autentica o usuário com base no CPF e senha.
        """
        cpf = self.cpf_entry.get()
        senha_hash = hash_senha(self.senha_entry.get())
        user = database.get_usuario(cpf)

        if user and user[3] == senha_hash:
            """
            Verifica se o CPF e a senha correspondem a um usuário no banco de dados.
            """
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            print("Autenticação bem-sucedida!") # Print somente para verificação no terminal
            self.controller.current_user_cpf = user[0]
            self.controller.show_frame("PainelUsuario")
        else:
            messagebox.showerror("Erro", "CPF ou senha inválidos.")