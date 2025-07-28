# Arquivo: pagina_emprestimos.py
# Classe de empréstimos do aplicativo

# Bibliotecas e Módulos
import tkinter as tk
from tkinter import messagebox
from pacotes import database
from .pagina_base import Base


class PaginaEmprestimos(Base):
    """
    Página de empréstimos do aplicativo.
    """
    def setup_widgets(self):

        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(fill="both", expand=True)
        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PainelUsuario"), bg="grey", fg="white").pack(pady=10, side="bottom")
    
    def on_show(self, data=None):

        for widget in self.main_frame.winfo_children(): widget.destroy()
        
        cpf = self.controller.current_user_cpf
        tk.Label(self.main_frame, text="Meus Empréstimos", font=("Arial", 20), bg="black", fg="red").pack(pady=10)
        emprestimos = database.get_emprestimos_ativos(cpf)
        
        if not emprestimos:
            """
            Verifica se o usuário possui empréstimos ativos.
            """
            tk.Label(self.main_frame, text="Você não possui empréstimos ativos.", bg="black", fg="white").pack(pady=10)
        
        else:
            """
            Exibe os empréstimos ativos do usuário caso existam.
            """
            for emp in emprestimos:
                id_emp, total, pago, p_totais, p_pagas = emp
                frame_emp = tk.Frame(self.main_frame, bg="#2a2a2a", pady=5)
                texto = f"ID: {id_emp} | Dívida: R${total-pago:.2f} ({p_pagas}/{p_totais} parcelas pagas)"
                tk.Label(frame_emp, text=texto, bg="#2a2a2a", fg="white").pack(side="left", padx=10)
                tk.Button(frame_emp, text="Pagar", bg="green", fg="white", command=lambda i=id_emp: self.controller.show_frame("PagarEmprestimo", data=i)).pack(side="right", padx=10)
                frame_emp.pack(fill="x", padx=20, pady=5)

        tk.Button(self.main_frame, text="Contratar Novo Empréstimo", command=lambda: self.controller.show_frame("Emprestimo"), bg="red", fg="white").pack(pady=20)
        