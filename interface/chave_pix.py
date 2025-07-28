# Arquivo: chave_pix.py
# Classe para gerenciar as chaves PIX do usuário

# Bibliotecas e Módulos
import tkinter as tk
import random
import string
from tkinter import messagebox
from pacotes import database
from .pagina_base import Base
import sqlite3

class ChavePix(Base):
    """
    Página para gerenciar as chaves PIX do usuário.
    """
    def setup_widgets(self):
        
        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(fill="both", expand=True)

        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PaginaPix"), bg="grey", fg="white").pack(pady=10, side="bottom")
    
    def on_show(self, data=None):
        
        for widget in self.main_frame.winfo_children(): 
            widget.destroy()
        
        cpf = self.controller.current_user_cpf
        tk.Label(self.main_frame, text="Minhas Chaves PIX", font=("Arial", 20), bg="black", fg="red").pack(pady=10)
        keys_frame = tk.LabelFrame(self.main_frame, text="Chaves Cadastradas", bg="black", fg="white", padx=10, pady=10)
        keys_frame.pack(pady=10, padx=10, fill="x")
        
        chaves = database.get_chaves_pix(cpf)
        
        if not chaves:
            tk.Label(keys_frame, text="Nenhuma chave cadastrada.", bg="black", fg="white").pack()
        else:
            for chave, tipo in chaves:
                tk.Label(keys_frame, text=f"{tipo}: {chave}", bg="black", fg="lightgrey").pack(anchor="w")
        
        register_frame = tk.LabelFrame(self.main_frame, text="Cadastrar Nova Chave", bg="black", fg="white", padx=10, pady=10)
        register_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Button(register_frame, text="Cadastrar E-mail da Conta", command=self.cadastrar_email, bg="red", fg="white").pack(fill="x", pady=2)
        tk.Button(register_frame, text="Cadastrar CPF da Conta", command=self.cadastrar_cpf, bg="red", fg="white").pack(fill="x", pady=2)
        tk.Button(register_frame, text="Gerar Chave Aleatória", command=self.gerar_aleatoria, bg="red", fg="white").pack(fill="x", pady=2)
        
        celular_frame = tk.Frame(register_frame, bg="black")
        self.celular_entry = tk.Entry(celular_frame, width=20)
        self.celular_entry.pack(side="left", fill="x", expand=True, padx=(0,5))
        
        tk.Button(celular_frame, text="Salvar Celular", command=self.cadastrar_celular, bg="#c00", fg="white").pack(side="left")
        celular_frame.pack(fill="x", pady=(5,2))

    def cadastrar_chave(self, chave, tipo):
        """
        Cadastra uma nova chave PIX para o usuário.
        """
        cpf = self.controller.current_user_cpf

        if not chave:  
            """
            Verifica se a chave está vazia.
            """
            messagebox.showerror("Erro", "O campo não pode estar vazio.")
            return
        try:
            """
            Verifica se a chave já existe ao tentar adiciona-la no banco de dados.
            """
            database.adicionar_chave_pix(chave, tipo, cpf)
            messagebox.showinfo("Sucesso", f"Chave '{tipo}' cadastrada com sucesso!")
            self.on_show()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Esta chave já está cadastrada no sistema.")

    def cadastrar_email(self):
        """
        Cadastra o e-mail do usuário como chave PIX.
        """
        self.cadastrar_chave(database.get_usuario(self.controller.current_user_cpf)[2], "E-mail")
    
    def cadastrar_cpf(self):
        """
        Cadastra o CPF do usuário como chave PIX.
        """
        self.cadastrar_chave(self.controller.current_user_cpf, "CPF")

    def cadastrar_celular(self):
        """
        Cadastra o número de celular do usuário como chave PIX.
        """
        celular = self.celular_entry.get()

        if not celular.isdigit() or len(celular) < 10:
            """
            Verifica se o número digitado é válido para um celular.
            """
            messagebox.showerror("Erro", "Número de celular inválido.")
            return
        self.cadastrar_chave(celular, "Celular")

    def gerar_aleatoria(self):
        """
        Gera uma chave PIX aleatória e a cadastra.
        """
        while True:
            chave = ''.join(random.choices(string.digits, k=6))

            if not database.Checar_se_a_chave_existe(chave):
                self.cadastrar_chave(chave, "Aleatória")
                break
