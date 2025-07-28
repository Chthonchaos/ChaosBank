# Arquivo: pagina_inicial.py
# Página inicial do aplicativo

# Bibliotecas e Módulos
import tkinter as tk
from tkinter import messagebox, ttk, Toplevel, Frame, Label, Button 
from .pagina_base import Base

class PaginaInicial(Base):
    """
    Página inicial do aplicativo.
    """
    def setup_widgets(self):
        """
        Configura os widgets da página inicial.
        """
        self.controller.configure(bg="black")
        logo = tk.Label(self, image=self.controller.logo_image, bg="black")
        logo.pack(pady=(50,0))
    
        tk.Label(self, text="Chaos Bank", font=("Arial", 26, "bold"), fg="red", bg="black").pack(pady=20)
        tk.Button(self, text="Login", command=lambda: self.controller.show_frame("Login"), bg="red", fg="white", font=("Arial", 12), width=20).pack(pady=8)
        tk.Button(self, text="Cadastrar", command=lambda: self.controller.show_frame("Cadastro"), bg="red", fg="white", font=("Arial", 12), width=20).pack(pady=8)
