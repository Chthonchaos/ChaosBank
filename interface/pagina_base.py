# Arquivo: pagina_base.py
# Classe base para todas as páginas do aplicativo

# Bibliotecas e Módulos
import tkinter as tk
from tkinter import messagebox
from pacotes import database

class Base(tk.Frame):
    """
    Classe base para todas as páginas.
    """
    def __init__(self, parent, controller, **kwargs):
        """
        Inicializa a classe base.
        """
        super().__init__(parent, bg="black", **kwargs)
        self.controller = controller
        self.setup_widgets()

    def setup_widgets(self):
        """Função para configuração dos widgets."""
        pass 

    def on_show(self, data=None):
        """Função chamada ao exibir a página."""
        pass