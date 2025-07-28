# Arquivo: painel_usuario.py
# Painel Principal do Banco

# Bibliotecas e Módulos
import tkinter as tk
from .pagina_base import Base

class PainelUsuario(Base):
    """
    Painel Principal do Banco.
    """
    def setup_widgets(self):

        tk.Label(self, text="Painel do Cliente", font=("Arial", 20), bg="black", fg="red").pack(pady=(40,15))

        botoes = [
            ("Saldo e Extrato", lambda: self.controller.show_frame("Extrato")),
            ("Transferência", lambda: self.controller.show_frame("Transferencia")),
            ("Empréstimos", lambda: self.controller.show_frame("Emprestimo")),
            ("Área PIX", lambda: self.controller.show_frame("PaginaPix")),
            ("Cartões Digitais", lambda: self.controller.show_frame("Cartoes")),
            ("Recarga de Celular", lambda: self.controller.show_frame("Recarga")),
        ]

        for texto, comando in botoes:
            tk.Button(self, text=texto, command=comando, bg="red", fg="white", width=20, font=("Arial", 11)).pack(pady=8)
        tk.Button(self, text="Sair (Logout)", command=self.logout, bg="grey", fg="white").pack(pady=(20,0))

    def logout(self):
        self.controller.current_user_cpf = None
        self.controller.show_frame("Login")
