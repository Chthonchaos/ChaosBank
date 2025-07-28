# Arquivo: transferencia.py
# Classe de transferência do aplicativo

# Bibliotecas e Módulos
import tkinter as tk
from tkinter import messagebox
from pacotes import database
from .pagina_base import Base
from pacotes.utils import gerar_comprovante

class Transferencia(Base):
    """
    Página de transferência do aplicativo.
    """
    def setup_widgets(self):

        tk.Label(self, text="Transferência", font=("Arial", 20), bg="black", fg="red").pack(pady=(40,15))
        tk.Label(self, text="CPF Destino:", bg="black", fg="white").pack()
        self.destino = tk.Entry(self, width=30)
        self.destino.pack()
        tk.Label(self, text="Valor:", bg="black", fg="white").pack()
        self.valor = tk.Entry(self, width=30)
        self.valor.pack()
        tk.Button(self, text="Transferir", command=self.transferir, bg="red", fg="white").pack(pady=10)
        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PainelUsuario"), bg="grey", fg="white").pack()
    
    def transferir(self):
        """
        Realiza a transferência entre contas.
        """
        cpf_origem = self.controller.current_user_cpf
        destino_cpf = self.destino.get()

        try:
            valor = float(self.valor.get())

            if valor <= 0: raise ValueError
            saldo_origem = database.get_usuario(cpf_origem)[4]

            if saldo_origem < valor:
                """
                Verifica se o saldo é suficiente para a transferência.
                """
                messagebox.showerror("Erro", "Saldo insuficiente.")
                return
            dest_user = database.get_usuario(destino_cpf)

            if not dest_user:
                """
                Verifica se o destinatário da transferência existe.
                """
                messagebox.showerror("Erro", "Destinatário não encontrado.")
                return

            database.atualizar_saldo(cpf_origem, -valor)
            database.atualizar_saldo(destino_cpf, valor)
            database.registrar_acao(cpf_origem, "transferencia_saida", -valor, f"Transferência para {dest_user[1]}")
            database.registrar_acao(destino_cpf, "transferencia_entrada", valor, f"Transferência de {database.get_usuario(cpf_origem)[1]}")
            messagebox.showinfo("Sucesso", "Transferência realizada.")
            gerar_comprovante(self, "Transferência", valor, cpf_origem, destino_cpf)
            
            self.controller.show_frame("PainelUsuario")

        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")
