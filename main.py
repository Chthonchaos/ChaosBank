# Arquivo: principal.py
# Autores: Matheus de Morais, Luan Victor

# Bibliotecas
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw

# Importa as classes e módulos
from pacotes.utils import hash_senha, mask_cpf, gerar_comprovante
import pacotes.database
from pacotes import database
from pacotes.database import (
    setup_database,
    get_usuario,
    get_usuario_por_email,
    get_extrato,
    get_emprestimos_ativos,
    get_emprestimo_por_id,
    registrar_acao,
    atualizar_saldo,
    registrar_novo_usuario,
    registrar_emprestimo,
    atualizar_emprestimo_pago,
    quitar_emprestimo,
    close_connection
)
from interface import *

class ChaosBank(tk.Tk):
    """
    Classe principal do aplicativo Chaos Bank.
    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.logo_image = self.criar_logo()
        if self.logo_image:
            self.iconphoto(False, self.logo_image)
        
        self.title("Chaos Bank")
        self.geometry("400x600")
        
        container = tk.Frame(self, bg="black")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.current_user_cpf = None

        frame_classes = [
            PaginaInicial, Login, Cadastro, PainelUsuario,
            Extrato, Transferencia, Emprestimo, PagarEmprestimo, PaginaEmprestimos, 
            PaginaPix, ChavePix, TransferenciaPix, Cartoes, Recarga,
        ]
        
        for F_class in frame_classes:

            page_name = F_class.__name__
            frame = F_class(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PaginaInicial")

    def criar_logo(self):
        """
        Cria a logo do aplicativo na PaginaInicial.
        """
        image = Image.new("RGB", (64, 64), "black")
        draw = ImageDraw.Draw(image)
        draw.text((12, 10), "C", fill="red", font_size=50)
        draw.text((32, 10), "B", fill="red", font_size=50)
        return ImageTk.PhotoImage(image)

    def show_frame(self, page_name, data=None):
    
        frame = self.frames[page_name]
        if hasattr(frame, 'on_show'):
            frame.on_show(data)
        frame.tkraise()

if __name__ == '__main__':
    """
    Inicializa o banco de dados e a aplicação.
    """
    database.setup_database()
    app = ChaosBank()

    """Função para quando fechar a janela pedir a confirmação do usuário."""
    def on_closing():

        if messagebox.askokcancel("Sair", "Deseja sair do Chaos Bank?"):
            database.close_connection()
            app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()