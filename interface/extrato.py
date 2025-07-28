# Arquivo: extrato.py
# Classe de extrato do aplicativo

# Bibliotecas e Módulos
import tkinter as tk
from tkinter import messagebox
from pacotes import database
from .pagina_base import Base
from datetime import datetime
from tkinter import ttk

class Extrato(Base):
    """
    Página de extrato do aplicativo.
    """
    def setup_widgets(self):

        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(fill="both", expand=True)

        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PainelUsuario"), bg="grey", fg="white").pack(pady=10, side="bottom")
    
    def on_show(self, data=None):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        cpf = self.controller.current_user_cpf
        tk.Label(self.main_frame, text="Saldo e Extrato", font=("Arial", 20), bg="black", fg="red").pack(pady=10)
        
        saldo = database.get_usuario(cpf)[4]
        tk.Label(self.main_frame, text=f"Saldo: R$ {saldo:.2f}", fg="white", bg="black", font=("Arial", 14, "bold")).pack(pady=10)
        
        extrato_frame = tk.Frame(self.main_frame, bg="black")
        extrato_frame.pack(fill="both", expand=True, padx=10, pady=5)
        canvas = tk.Canvas(extrato_frame, bg="black", highlightthickness=0)
        
        scrollbar = ttk.Scrollbar(extrato_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="black")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        extrato = database.get_extrato(cpf)
        
        if not extrato:
            """
            Verifica se há transações no extrato.
            """
            tk.Label(scrollable_frame, text="Nenhuma transação encontrada.", bg="black", fg="white").pack()
        
        else:
            """
            Exibe as transações no extrato caso existam.
            """
            for tipo, valor, descricao, data_str in extrato:
                data_f = datetime.strptime(data_str.split('.')[0], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%y %H:%M')
                cor = "lightgreen" if valor > 0 else "lightcoral"
                sinal = "+" if valor > 0 else ""
                texto = f"{data_f} - {tipo.upper()}\n{descricao}\nValor: {sinal}R$ {valor:.2f}"
                tk.Label(scrollable_frame, text=texto, bg="#2a2a2a", fg=cor, anchor="w", justify="left", padx=10, pady=5).pack(fill="x", pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
