import tkinter as tk
from tkinter import messagebox
from pacotes import database
from pacotes.utils import hash_senha, mask_cpf, gerar_comprovante
from .pagina_base import Base 


class PagarEmprestimo (Base):
    """
    Página de pagamento de empréstimo do aplicativo.
    """
    def setup_widgets(self):

        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(fill="both", expand=True)

        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PaginaEmprestimos"), bg="grey", fg="white").pack(pady=20, side="bottom")

    def on_show(self, data):

        self.pagamento = data
        
        for widget in self.main_frame.winfo_children(): 
            widget.destroy()

        self.emprestimo = database.get_emprestimo_por_id(self.pagamento)
        
        if not self.emprestimo: 
            return 
        
        id_emp, _, _, total_a_pagar, pago, p_totais, p_pagas, v_parcela, _ = self.emprestimo
        restante = total_a_pagar - pago
        
        tk.Label(self.main_frame, text=f"Pagar Empréstimo #{id_emp}", font=("Arial", 20), bg="black", fg="red").pack(pady=10)
        tk.Label(self.main_frame, text=f"Valor restante: R$ {restante:.2f}", font=("Arial", 12), bg="black", fg="white").pack()
        tk.Label(self.main_frame, text=f"Parcelas: {p_pagas}/{p_totais}", font=("Arial", 10), bg="black", fg="white").pack(pady=(0, 20))
        
        tk.Button(self.main_frame, text=f"Pagar 1 Parcela (R$ {v_parcela:.2f})", command=self.pagar_parcela, bg="red", fg="white").pack(pady=10)
        tk.Button(self.main_frame, text=f"Quitar Empréstimo (R$ {restante:.2f})", command=self.quitar_total, bg="darkred", fg="white").pack(pady=5)
    
    def pagar_parcela(self):
        """
        Realiza o pagamento de uma parcela do empréstimo.
        """
        cpf = self.controller.current_user_cpf
        valor_pagar = self.emprestimo[7]
        saldo_usuario = database.get_usuario(cpf)[4]
        
        if saldo_usuario < valor_pagar:
            """
            Verifica se o saldo do usuário é suficiente para pagar a parcela.
            """
            messagebox.showerror("Erro", "Saldo insuficiente para pagar a parcela.")
            return
        
        database.atualizar_saldo(cpf, -valor_pagar)
        database.atualizar_emprestimo_pago(self.pagamento, valor_pagar)
        database.registrar_acao(cpf, "pagamento", -valor_pagar, f"Pagamento parcela empréstimo #{self.pagamento}")
        
        if self.emprestimo[6] + 1 == self.emprestimo[5]:
            """
            Verifica se todas as parcelas do empréstimo foram pagas.
            """
            database.quitar_emprestimo(self.pagamento)

        messagebox.showinfo("Sucesso", "Parcela paga com sucesso!")
        self.controller.show_frame("PaginaEmprestimos")

    def quitar_total(self):
        """
        Quita o empréstimo total.
        """
        cpf = self.controller.current_user_cpf
        valor_quitar = self.emprestimo[3] - self.emprestimo[4]
        saldo_usuario = database.get_usuario(cpf)[4]
        
        if saldo_usuario < valor_quitar:
            """
            Verifica se o saldo do usuário é suficiente para quitar o empréstimo.
            """
            messagebox.showerror("Erro", "Saldo insuficiente para quitar o empréstimo.")
            return
        
        database.atualizar_saldo(cpf, -valor_quitar)
        database.quitar_emprestimo(self.pagamento)
        database.registrar_acao(cpf, "pagamento", -valor_quitar, f"Quitação empréstimo #{self.pagamento}")
        messagebox.showinfo("Sucesso", "Empréstimo quitado com sucesso!")
        self.controller.show_frame("PaginaEmprestimos")
