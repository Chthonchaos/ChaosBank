# Arquivo: recarga.py
# Página para recarga de celular do usuário

# Bibliotecas e Módulos
import tkinter as tk
from tkinter import messagebox
from pacotes import database
from .pagina_base import Base

class Recarga(Base):
    """
    Página para recarga de celular do usuário.
    """
    def setup_widgets(self):

        tk.Label(self, text="Recarga de Celular", font=("Arial", 20), bg="black", fg="red").pack(pady=(40,15))
        tk.Label(self, text="Número com DDD (só dígitos):", bg="black", fg="white").pack()
        self.numero_cel = tk.Entry(self, width=30)
        self.numero_cel.pack()

        tk.Label(self, text="Valor da Recarga:", bg="black", fg="white").pack()
        self.valor = tk.Entry(self, width=30)
        self.valor.pack()

        tk.Button(self, text="Recarregar", command=self.recarregar, bg="red", fg="white").pack(pady=10)
        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PainelUsuario"), bg="grey", fg="white").pack()
    
    def recarregar(self):
        """
        Realiza a recarga de celular do usuário.
        """
        cpf = self.controller.current_user_cpf
        numero = self.numero_cel.get()

        try:
            valor = float(self.valor.get())
            
            if not numero.isdigit() or len(numero) not in [10, 11] or valor <= 0:
                """
                Verifica se o número de celular e o valor da recarga são válidos.
                """
                raise ValueError
            saldo_usuario = database.get_usuario(cpf)[4]
            
            if saldo_usuario < valor:
                """
                Verifica se o saldo do usuário é suficiente para realizar a recarga.
                """
                messagebox.showerror("Erro", "Saldo insuficiente.")
                return
            
            database.atualizar_saldo(cpf, -valor)
            database.registrar_acao(cpf, "recarga", -valor, f"Recarga de celular para o número {numero}")
            messagebox.showinfo("Sucesso", f"Recarga de R$ {valor:.2f} realizada para o número {numero}!")
            self.controller.show_frame("PainelUsuario")
        except ValueError:
            messagebox.showerror("Erro", "Número ou valor inválido.")