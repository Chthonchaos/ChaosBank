# Arquivo: pagina_pix.py
# Página para realizar operações com PIX

# Bibliotecas e Módulos
import tkinter as tk
from .pagina_base import Base

class PaginaPix(Base):
    """
    Página para realizar operações com PIX.
    """
    def setup_widgets(self):

        tk.Label(self, text="Área PIX", font=("Arial", 24, "bold"), bg="black", fg="red").pack(pady=(40, 20))
        tk.Button(self, text="Enviar PIX", command=lambda: self.controller.show_frame("TransferenciaPix"), bg="red", fg="white", font=("Arial", 12), width=25, height=2).pack(pady=10)
        tk.Button(self, text="Gerenciar Minhas Chaves", command=lambda: self.controller.show_frame("ChavePix"), bg="red", fg="white", font=("Arial", 12), width=25, height=2).pack(pady=10)
        tk.Button(self, text="Voltar ao Painel", command=lambda: self.controller.show_frame("PainelUsuario"), bg="grey", fg="white", font=("Arial", 10)).pack(pady=(30, 0))
