# Arquivo: cartoes.py
# Classe de cartões

# Bibliotecas e Módulos
import sqlite3
import tkinter as tk
import random
import string
from tkinter import messagebox
from pacotes import database
from .pagina_base import Base

class Cartoes(Base):
    """
    Página para gerenciar cartões digitais do usuário.
    """
    def setup_widgets(self):

        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(fill="both", expand=True)
        
        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PainelUsuario"), bg="grey", fg="white").pack(pady=10, side="bottom")
    
    def on_show(self, data=None):

        for widget in self.main_frame.winfo_children(): 
            widget.destroy()
        
        cpf = self.controller.current_user_cpf
        tk.Label(self.main_frame, text="Cartões Digitais", font=("Arial", 20), bg="black", fg="red").pack(pady=10)
        cartoes = database.get_cartoes(cpf)
        
        if not cartoes:
            tk.Label(self.main_frame, text="Nenhum cartão gerado.", bg="black", fg="white").pack(pady=10)
        else:
            for cartao in cartoes:
                num, val, cvv, tipo, limite = cartao
                frame_cartao = tk.Frame(self.main_frame, bg="#2a2a2a", pady=10)
                texto = f"Tipo: {tipo.title()}\nFinal: {num[-4:]}\nValidade: {val} | CVV: {cvv}"
                
                if tipo == 'credito':
                    texto += f"\nLimite: R$ {limite:.2f}"
                
                tk.Label(frame_cartao, text=texto, bg="#2a2a2a", fg="white", justify="left").pack(padx=10)
                frame_cartao.pack(fill="x", padx=20, pady=5)
        
        tk.Button(self.main_frame, text="Gerar Novo Cartão de Crédito", command=lambda: self.gerar_cartao('credito'), bg="red", fg="white").pack(pady=10)
    
    def gerar_cartao(self, tipo):
        """
        Gera um novo cartão de crédito para o usuário.
        """
        cpf = self.controller.current_user_cpf
        numero = "4" + "".join(random.choices(string.digits, k=15))
        validade = f"{random.randint(1,12):02d}/{random.randint(26, 30)}"
        cvv = "".join(random.choices(string.digits, k=3))
        limite = 500.0
        
        try:
            """
            Registra o novo cartão no banco de dados.
            """
            database.registrar_cartao(cpf, numero, validade, cvv, tipo, limite)
            messagebox.showinfo("Sucesso", "Novo cartão de crédito gerado!")
            self.on_show() 
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Não foi possível gerar o cartão. Tente novamente.")
