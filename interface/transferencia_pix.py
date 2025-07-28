# Arquivo: transferencia_pix.py
# Página para enviar PIX

# Bibliotecas e Módulos
import tkinter as tk
from tkinter import messagebox
from pacotes import database
from .pagina_base import Base
from pacotes.utils import gerar_comprovante

class TransferenciaPix(Base):
    """
    Página para enviar PIX.
    """
    def setup_widgets(self):

        tk.Label(self, text="Enviar PIX", font=("Arial", 20), bg="black", fg="red").pack(pady=(40,15))
        tk.Label(self, text="Chave PIX Destino:", bg="black", fg="white").pack()
        self.chave = tk.Entry(self, width=30)
        self.chave.pack()
        
        tk.Label(self, text="Valor:", bg="black", fg="white").pack()
        self.valor = tk.Entry(self, width=30)
        self.valor.pack()
        
        tk.Button(self, text="Enviar PIX", command=self.enviar_pix, bg="red", fg="white").pack(pady=10)
        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PaginaPix"), bg="grey", fg="white").pack()
    
    def enviar_pix(self):
        """ 
        Envia um PIX para a chave digitada.
        """
        cpf_origem = self.controller.current_user_cpf
        chave = self.chave.get()
        
        try:
            valor = float(self.valor.get())
            
            if valor <= 0: raise ValueError
            saldo_origem = database.get_usuario(cpf_origem)[4]
            
            if saldo_origem < valor:
                """
                Verifica se o saldo do usuário é suficiente para enviar o PIX.
                """
                messagebox.showerror("Erro", "Saldo insuficiente.")
                return
            
            resultado = database.get_pix_destino(chave)
            
            if not resultado:
                """
                Verifica se a chave PIX de destino existe no banco de dados.
                """
                messagebox.showerror("Erro", "Chave PIX não encontrada.")
                return
            
            destino_cpf = resultado[0]
            dest_user = database.get_usuario(destino_cpf)
            database.atualizar_saldo(cpf_origem, -valor)
            database.atualizar_saldo(destino_cpf, valor)
            database.registrar_acao(cpf_origem, "pix_saida", -valor, f"PIX enviado para {dest_user[1]}")
            database.registrar_acao(destino_cpf, "pix_entrada", valor, f"PIX recebido de {database.get_usuario(cpf_origem)[1]}")

            messagebox.showinfo("Sucesso", "PIX enviado com sucesso.")
            gerar_comprovante(self, "PIX", valor, cpf_origem, chave)

            self.controller.show_frame("PaginaPix")
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")
