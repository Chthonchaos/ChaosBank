# Arquivo: emprestimo.py
# Classe de empréstimo do aplicativo

# Bibliotecas e Módulos
import tkinter as tk
from tkinter import messagebox
from pacotes import database
from .pagina_base import Base


class Emprestimo(Base):
    """
    Página de contratação de empréstimo do aplicativo.
    """
    def setup_widgets(self):

        tk.Label(self, text="Contratar Empréstimo (Juros 5%)", font=("Arial", 20), bg="black", fg="red").pack(pady=(40,15))
        tk.Label(self, text="Valor do Empréstimo:", bg="black", fg="white").pack()
        self.valor = tk.Entry(self, width=30)
        self.valor.pack()
        
        tk.Label(self, text="Número de Parcelas (até 48x):", bg="black", fg="white").pack()
        self.parcelas = tk.Entry(self, width=30)
        self.parcelas.pack()
        
        tk.Button(self, text="Simular e Contratar", command=self.contratar, bg="red", fg="white").pack(pady=10)
        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PaginaEmprestimos"), bg="grey", fg="white").pack()

    def contratar(self):
        """
        Contrata um novo empréstimo.
        """
        cpf = self.controller.current_user_cpf
        
        try:
            valor = float(self.valor.get())
            parcelas = int(self.parcelas.get())
            
            if not (0 < valor <= 50000) or not (0 < parcelas <= 48):
                """
                Verifica se os valores estão dentro dos limites permitidos pelo banco.
                """
                raise ValueError("Valores fora do limite.")
            
            juros = 0.05
            total_a_pagar = valor * ((1 + juros) ** parcelas)
            valor_parcela = total_a_pagar / parcelas
            
            confirm = messagebox.askyesno("Confirmar Empréstimo", f"Valor: R${valor:.2f}\nTotal a pagar: R${total_a_pagar:.2f}\n{parcelas}x de R${valor_parcela:.2f}\n\nDeseja contratar?")
            
            if confirm:
                """
                Verifica a confirmação do empréstimo e o registra no banco de dados.
                """
                database.atualizar_saldo(cpf, valor)
                database.registrar_acao(cpf, "emprestimo", valor, f"Empréstimo contratado de R${valor:.2f}")
                database.registrar_emprestimo(cpf, valor, total_a_pagar, parcelas, valor_parcela)
                messagebox.showinfo("Aprovado", f"Empréstimo de R$ {valor:.2f} creditado em sua conta!")
                self.controller.show_frame("PaginaEmprestimos")
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos.")
