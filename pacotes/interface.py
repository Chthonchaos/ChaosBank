# Arquivo: interface.py
# Interface gráfica

# Bibliotecas e Módulos
import tkinter as tk
from tkinter import messagebox, ttk, Toplevel, Frame, Label, Button
import random
import string
import sqlite3
from datetime import datetime
from pacotes import utils
from pacotes.utils import hash_senha, mask_cpf, gerar_comprovante, send_recovery_email
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
    salvar_codigo_recuperacao,
    verificar_codigo_recuperacao,
    redefinir_senha,
    close_connection
)

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

    def setup_widgets(self): pass # Função para configuração dos widgets nas telas.
    def on_show(self, data=None): pass # Função para exibir as páginas.

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

class Login(Base):
    """
    Página de login do aplicativo.
    """
    def setup_widgets(self):
    """
    Configura os widgets da página de login...
    """
        tk.Label(self, text="Login", font=("Arial", 20), bg="black", fg="red").pack(pady=(40,15))

        tk.Label(self, text="CPF:", bg="black", fg="white").pack()
        self.cpf_entry = tk.Entry(self, width=30)
        self.cpf_entry.pack()

        tk.Label(self, text="Senha:", bg="black", fg="white").pack()
        self.senha_entry = tk.Entry(self, show="*", width=30)
        self.senha_entry.pack()

        tk.Button(self, text="Entrar", command=self.autenticar, bg="red", fg="white").pack(pady=10)
        tk.Button(self, text="Esqueci minha senha", command=lambda: self.controller.show_frame("RecuperacaoSenha"), bg="#333", fg="white", bd=0, activebackground="#333", activeforeground="red").pack()
        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PaginaInicial"), bg="grey", fg="white").pack(pady=(20,0))
    
    def autenticar(self):
        """
        Autentica o usuário com base no CPF e senha.
        """
        cpf = self.cpf_entry.get()
        senha_hash = hash_senha(self.senha_entry.get())
        user = database.get_usuario(cpf)

        if user and user[3] == senha_hash:
            print("Autenticação bem-sucedida!")
            self.controller.current_user_cpf = user[0]
            self.controller.show_frame("PainelUsuario")
        else:
            messagebox.showerror("Erro", "CPF ou senha inválidos.")


class Cadastro(Base):
    """
    Página de cadastro do aplicativo.
    """
    def setup_widgets(self):

        tk.Label(self, text="Cadastro", font=("Arial", 20), bg="black", fg="red").pack(pady=(40,15))
        campos = ["CPF (só números)", "Nome Completo", "Email", "Senha"]
        self.entradas = {}

        for campo in campos:
            tk.Label(self, text=f"{campo}:", bg="black", fg="white", font=("Arial", 10)).pack()
            entry = tk.Entry(self, show="*" if campo == "Senha" else None, width=30)
            entry.pack(pady=3)
            self.entradas[campo.split(' ')[0].lower()] = entry

        tk.Button(self, text="Registrar", command=self.registrar, bg="red", fg="white").pack(pady=10)
        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PaginaInicial"), bg="grey", fg="white").pack()

    def registrar(self):
        """
        Registra um novo usuário.
        """
        dados = {campo: entry.get() for campo, entry in self.entradas.items()}
        
        if not all(dados.values()):
            """        
            Verifica se todos os campos foram preenchidos.
            """
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return
        
        cpf = dados['cpf']

        if not cpf.isdigit() or len(cpf) != 11: 
            """
            Verifica se o CPF tem o formato válido, ou seja, possui apenas números e 11 dígitos.
            """
            messagebox.showerror("Erro de Cadastro", "CPF inválido. Digite apenas 11 números.")
            return

        email = dados['email']
        dominios_validos = ["@gmail.com", "@hotmail.com", "@yahoo.com", "@outlook.com", "@live.com"]

        if "@" not in email or not any(email.endswith(dominio) for dominio in dominios_validos):
            """
            Verifica se o e-mail contém um dos domínios válidos.
            """
            messagebox.showerror("Erro de Cadastro", "Formato de e-mail inválido ou domínio não suportado.")
            return

        senha = dados['senha']
        
        if len(senha) < 6:
            """
            Verifica se a senha no mínimo 6 caracteres.
            """
            messagebox.showerror("Erro de Cadastro", "A senha deve ter no mínimo 6 caracteres.")
            return

        try:
            """
            Adiciona o novo usuário no banco de dados.
            """
            database.registrar_novo_usuario(dados['cpf'], dados['nome'], dados['email'], hash_senha(dados['senha']))
            database.adicionar_chave_pix(dados['cpf'], 'CPF', dados['cpf'])
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            self.controller.show_frame("Login")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF ou Email já cadastrado.")


class RecuperacaoSenha(Base):
    """
    Página de recuperação de senha do aplicativo.
    """
    def setup_widgets(self):

        tk.Label(self, text="Recuperar Senha", font=("Arial", 20), bg="black", fg="red").pack(pady=(40,15))
        self.user_email = ""
        self.frame_email = tk.Frame(self, bg="black")

        tk.Label(self.frame_email, text="Digite seu e-mail cadastrado:", bg="black", fg="white").pack()
        self.email_entry = tk.Entry(self.frame_email, width=30)
        self.email_entry.pack()

        tk.Button(self.frame_email, text="Enviar Código", command=self.codigo, bg="red", fg="white").pack(pady=10)
        self.frame_email.pack()
        self.frame_code = tk.Frame(self, bg="black")

        tk.Label(self.frame_code, text="Digite o código recebido:", bg="black", fg="white").pack()
        self.code_entry = tk.Entry(self.frame_code, width=30)
        self.code_entry.pack()

        tk.Button(self.frame_code, text="Verificar Código", command=self.codigo_verificacao, bg="red", fg="white").pack(pady=10)
        self.frame_password = tk.Frame(self, bg="black")

        tk.Label(self.frame_password, text="Digite sua nova senha:", bg="black", fg="white").pack()
        self.new_pass_entry = tk.Entry(self.frame_password, show="*", width=30)
        self.new_pass_entry.pack()

        tk.Label(self.frame_password, text="Confirme a nova senha:", bg="black", fg="white").pack()
        self.confirm_pass_entry = tk.Entry(self.frame_password, show="*", width=30)
        self.confirm_pass_entry.pack()

        tk.Button(self.frame_password, text="Redefinir Senha", command=self.resetar_senha, bg="red", fg="white").pack(pady=10)
        tk.Button(self, text="Voltar para o Login", command=lambda: self.controller.show_frame("Login"), bg="grey", fg="white").pack(pady=20)
    
    def on_show(self, data=None):

        self.frame_password.pack_forget()
        self.frame_code.pack_forget()
        self.frame_email.pack()
        self.email_entry.delete(0, tk.END)
        self.code_entry.delete(0, tk.END)
        self.new_pass_entry.delete(0, tk.END)
        self.confirm_pass_entry.delete(0, tk.END)

    def codigo(self):
        """
        Envia um código de recuperação para o e-mail do usuário.
        """
        self.user_email = self.email_entry.get()
        user = database.get_usuario_por_email(self.user_email)

        if not user:
            """
            Verifica se o e-mail do usuário existe no banco de dados.
            """
            messagebox.showerror("Erro", "E-mail não encontrado.")
            return

        recovery_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        if send_recovery_email(self.user_email, user[1], recovery_code):
            database.salvar_codigo_recuperacao(self.user_email, recovery_code)
            messagebox.showinfo("Sucesso", "Um código de recuperação foi enviado para seu e-mail.")
            self.frame_email.pack_forget()
            self.frame_code.pack()

    def codigo_verificacao(self):
        """
        Verifica o código de recuperação enviado para o e-mail do usuário.
        """
        code = self.code_entry.get()

        if database.verificar_codigo_recuperacao(self.user_email, code):
            self.frame_code.pack_forget()
            self.frame_password.pack()
        else:
            messagebox.showerror("Erro", "Código inválido ou expirado.")

    def resetar_senha(self):
        """
        Redefine a senha do usuário.
        """
        new_pass = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()

        if new_pass != confirm_pass:
            """
            Verifica se as senhas são iguais.
            """
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        if len(new_pass) < 6:
            """
            Verifica se a nova senha tem o mínimo de 6 caracteres.
            """
            messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres.")
            return

        database.redefinir_senha(self.user_email, hash_senha(new_pass))
        messagebox.showinfo("Sucesso", "Senha redefinida com sucesso!")
        self.controller.show_frame("Login")

class PainelUsuario(Base):
    """
    Painel Principal do Banco.
    """
    def setup_widgets(self):

        tk.Label(self, text="Painel do Cliente", font=("Arial", 20), bg="black", fg="red").pack(pady=(40,15))

        botoes = [
            ("Saldo e Extrato", lambda: self.controller.show_frame("Extrato")),
            ("Transferência", lambda: self.controller.show_frame("Transferencia")),
            ("Empréstimos", lambda: self.controller.show_frame("Emprestimo")),
            ("Área PIX", lambda: self.controller.show_frame("PaginaPix")),
            ("Cartões Digitais", lambda: self.controller.show_frame("Cartoes")),
            ("Recarga de Celular", lambda: self.controller.show_frame("Recarga")),
        ]

        for texto, comando in botoes:
            tk.Button(self, text=texto, command=comando, bg="red", fg="white", width=20, font=("Arial", 11)).pack(pady=8)
        tk.Button(self, text="Sair (Logout)", command=self.logout, bg="grey", fg="white").pack(pady=(20,0))

    def logout(self):
        self.controller.current_user_cpf = None
        self.controller.show_frame("Login")


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


class Emprestimo(Base):
    """
    Página de contratação de empréstimo do aplicativo.
    """
    def setup_widgets(self):

        tk.Label(self, text="Contratar Empréstimo", font=("Arial", 20), bg="black", fg="red").pack(pady=(40,15))
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

class PaginaPix(Base):
    """
    Página para realizar operações com PIX.
    """
    def setup_widgets(self):

        tk.Label(self, text="Área PIX", font=("Arial", 24, "bold"), bg="black", fg="red").pack(pady=(40, 20))
        tk.Button(self, text="Enviar PIX", command=lambda: self.controller.show_frame("TransferenciaPix"), bg="red", fg="white", font=("Arial", 12), width=25, height=2).pack(pady=10)
        tk.Button(self, text="Gerenciar Minhas Chaves", command=lambda: self.controller.show_frame("ChavePix"), bg="red", fg="white", font=("Arial", 12), width=25, height=2).pack(pady=10)
        tk.Button(self, text="Voltar ao Painel", command=lambda: self.controller.show_frame("PainelUsuario"), bg="grey", fg="white", font=("Arial", 10)).pack(pady=(30, 0))


class ChavePix(Base):
    """
    Página para gerenciar as chaves PIX do usuário.
    """
    def setup_widgets(self):
        
        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(fill="both", expand=True)

        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PaginaPix"), bg="grey", fg="white").pack(pady=10, side="bottom")
    
    def on_show(self, data=None):
        
        for widget in self.main_frame.winfo_children(): 
            widget.destroy()
        
        cpf = self.controller.current_user_cpf
        tk.Label(self.main_frame, text="Minhas Chaves PIX", font=("Arial", 20), bg="black", fg="red").pack(pady=10)
        keys_frame = tk.LabelFrame(self.main_frame, text="Chaves Cadastradas", bg="black", fg="white", padx=10, pady=10)
        keys_frame.pack(pady=10, padx=10, fill="x")
        
        chaves = database.get_chaves_pix(cpf)
        
        if not chaves:
            tk.Label(keys_frame, text="Nenhuma chave cadastrada.", bg="black", fg="white").pack()
        else:
            for chave, tipo in chaves:
                tk.Label(keys_frame, text=f"{tipo}: {chave}", bg="black", fg="lightgrey").pack(anchor="w")
        
        register_frame = tk.LabelFrame(self.main_frame, text="Cadastrar Nova Chave", bg="black", fg="white", padx=10, pady=10)
        register_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Button(register_frame, text="Cadastrar E-mail da Conta", command=self.cadastrar_email, bg="red", fg="white").pack(fill="x", pady=2)
        tk.Button(register_frame, text="Cadastrar CPF da Conta", command=self.cadastrar_cpf, bg="red", fg="white").pack(fill="x", pady=2)
        tk.Button(register_frame, text="Gerar Chave Aleatória", command=self.gerar_aleatoria, bg="red", fg="white").pack(fill="x", pady=2)
        
        celular_frame = tk.Frame(register_frame, bg="black")
        self.celular_entry = tk.Entry(celular_frame, width=20)
        self.celular_entry.pack(side="left", fill="x", expand=True, padx=(0,5))
        
        tk.Button(celular_frame, text="Salvar Celular", command=self.cadastrar_celular, bg="#c00", fg="white").pack(side="left")
        celular_frame.pack(fill="x", pady=(5,2))

    def cadastrar_chave(self, chave, tipo):
        """
        Cadastra uma nova chave PIX para o usuário.
        """
        cpf = self.controller.current_user_cpf

        if not chave:  
            """
            Verifica se a chave está vazia.
            """
            messagebox.showerror("Erro", "O campo não pode estar vazio.")
            return
        try:
            database.adicionar_chave_pix(chave, tipo, cpf)
            messagebox.showinfo("Sucesso", f"Chave '{tipo}' cadastrada com sucesso!")
            self.on_show()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Esta chave já está cadastrada no sistema.")

    def cadastrar_email(self):
        """
        Cadastra o e-mail do usuário como chave PIX.
        """
        self.cadastrar_chave(database.get_usuario(self.controller.current_user_cpf)[2], "E-mail")
    
    def cadastrar_cpf(self):
        """
        Cadastra o CPF do usuário como chave PIX.
        """
        self.cadastrar_chave(self.controller.current_user_cpf, "CPF")

    def cadastrar_celular(self):
        """
        Cadastra o número de celular do usuário como chave PIX.
        """
        celular = self.celular_entry.get()

        if not celular.isdigit() or len(celular) < 10:
            """
            Verifica se o número digitado é válido para um celular.
            """
            messagebox.showerror("Erro", "Número de celular inválido.")
            return
        self.cadastrar_chave(celular, "Celular")

    def gerar_aleatoria(self):
        """
        Gera uma chave PIX aleatória e a cadastra.
        """
        while True:
            chave = ''.join(random.choices(string.digits, k=6))

            if not database.Checar_se_a_chave_existe(chave):
                self.cadastrar_chave(chave, "Aleatória")
                break


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

class Cartoes(Base):
    """
    Página para gerenciar cartões digitais do usuário.
    """
    def setup_widgets(self):

        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(fill="both", expand=True)
        
        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PainelUsuario"), bg="grey", fg="white").pack(pady=10, side="bottom")
    
    def on_show(self, data=None):

        for widget in self.main_frame.winfo_children(): 
            widget.destroy()
        
        cpf = self.controller.current_user_cpf
        tk.Label(self.main_frame, text="Cartões Digitais", font=("Arial", 20), bg="black", fg="red").pack(pady=10)
        cartoes = database.get_cartoes(cpf)
        
        if not cartoes:
            tk.Label(self.main_frame, text="Nenhum cartão gerado.", bg="black", fg="white").pack(pady=10)
        else:
            for cartao in cartoes:
                num, val, cvv, tipo, limite = cartao
                frame_cartao = tk.Frame(self.main_frame, bg="#2a2a2a", pady=10)
                texto = f"Tipo: {tipo.title()}\nFinal: {num[-4:]}\nValidade: {val} | CVV: {cvv}"
                
                if tipo == 'credito':
                    texto += f"\nLimite: R$ {limite:.2f}"
                
                tk.Label(frame_cartao, text=texto, bg="#2a2a2a", fg="white", justify="left").pack(padx=10)
                frame_cartao.pack(fill="x", padx=20, pady=5)
        
        tk.Button(self.main_frame, text="Gerar Novo Cartão de Crédito", command=lambda: self.gerar_cartao('credito'), bg="red", fg="white").pack(pady=10)
    
    def gerar_cartao(self, tipo):
        """
        Gera um novo cartão de crédito para o usuário.
        """
        cpf = self.controller.current_user_cpf
        numero = "4" + "".join(random.choices(string.digits, k=15))
        validade = f"{random.randint(1,12):02d}/{random.randint(26, 30)}"
        cvv = "".join(random.choices(string.digits, k=3))
        limite = 500.0
        
        try:
            database.registrar_cartao(cpf, numero, validade, cvv, tipo, limite)
            messagebox.showinfo("Sucesso", "Novo cartão de crédito gerado!")
            self.on_show() 
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Não foi possível gerar o cartão. Tente novamente.")


class Recarga(Base):
    """
    Página para recarga de celular do usuário.
    """
    def setup_widgets(self):

        tk.Label(self, text="Recarga de Celular", font=("Arial", 20), bg="black", fg="red").pack(pady=(40,15))
        tk.Label(self, text="Número com DDD (só dígitos):", bg="black", fg="white").pack()
        self.numero_cel = tk.Entry(self, width=30)
        self.numero_cel.pack()

        tk.Label(self, text="Valor da Recarga:", bg="black", fg="white").pack()
        self.valor = tk.Entry(self, width=30)
        self.valor.pack()

        tk.Button(self, text="Recarregar", command=self.recarregar, bg="red", fg="white").pack(pady=10)
        tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("PainelUsuario"), bg="grey", fg="white").pack()
    
    def recarregar(self):
        """
        Realiza a recarga de celular do usuário.
        """
        cpf = self.controller.current_user_cpf
        numero = self.numero_cel.get()

        try:
            valor = float(self.valor.get())
            
            if not numero.isdigit() or len(numero) not in [10, 11] or valor <= 0:
                """
                Verifica se o número de celular e o valor da recarga são válidos.
                """
                raise ValueError
            saldo_usuario = database.get_usuario(cpf)[4]
            
            if saldo_usuario < valor:
                """
                Verifica se o saldo do usuário é suficiente para realizar a recarga.
                """
                messagebox.showerror("Erro", "Saldo insuficiente.")
                return
            
            database.atualizar_saldo(cpf, -valor)
            database.registrar_acao(cpf, "recarga", -valor, f"Recarga de celular para o número {numero}")
            messagebox.showinfo("Sucesso", f"Recarga de R$ {valor:.2f} realizada para o número {numero}!")
            self.controller.show_frame("PainelUsuario")
        except ValueError:
            messagebox.showerror("Erro", "Número ou valor inválido.")