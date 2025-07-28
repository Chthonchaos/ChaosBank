# Arquivo: utils.py


#Biblioteca e Módulos
import hashlib
import smtplib
import ssl
from tkinter import Toplevel, Frame, Label, Button, messagebox
from datetime import datetime
from pacotes import database

# Função para gerar um hash para a senha
def hash_senha(senha):
    "Gera um hash  para a senha."
    return hashlib.sha256(senha.encode()).hexdigest()

# Função para mascarar o CPF
def mask_cpf(cpf):
    "Esconde o CPF."
    if isinstance(cpf, str) and len(cpf) == 11 and cpf.isdigit():
        return f"{cpf[:3]}.XXX.XXX-{cpf[9:]}"
    return cpf

# Função para gerar um comprovante de transação
def gerar_comprovante(janela_pai, tipo_transacao, valor, origem_cpf, destino_info, sucesso=True):
    "Cria uma nova janela para exibir um comprovante de transação."
    comprovante_window = Toplevel(janela_pai)
    comprovante_window.title(f"Comprovante de {tipo_transacao}")
    comprovante_window.geometry("350x450")
    comprovante_window.configure(bg="white")
    comprovante_window.resizable(False, False)
    comprovante_window.transient(janela_pai)
    comprovante_window.grab_set()

    header_frame = Frame(comprovante_window, bg="#1a1a1a", height=80)
    header_frame.pack(fill="x")
    Label(header_frame, text="Chaos Bank", font=("Arial", 20, "bold"), fg="red", bg="#1a1a1a").pack(pady=20)
    
    usuario_origem = database.get_usuario(origem_cpf)
    
    Label(comprovante_window, text=f"COMPROVANTE DE {tipo_transacao.upper()}", font=("Arial", 12, "bold"), bg="white").pack(pady=10)
    
    status_text = "Transação realizada com sucesso!" if sucesso else "Falha na transação"
    status_color = "green" if sucesso else "red"
    Label(comprovante_window, text=status_text, font=("Arial", 10, "bold"), fg=status_color, bg="white").pack()

    Label(comprovante_window, text=f"Valor: R$ {valor:.2f}", font=("Arial", 16, "bold"), bg="white").pack(pady=15)

    info_frame = Frame(comprovante_window, bg="white")
    info_frame.pack(pady=10, padx=20, fill="x")

    Label(info_frame, text="Origem", font=("Arial", 11, "bold"), bg="white", anchor="w").pack(fill="x")
    Label(info_frame, text=f"Nome: {usuario_origem[1]}", bg="white", anchor="w").pack(fill="x")
    Label(info_frame, text=f"CPF: {mask_cpf(origem_cpf)}", bg="white", anchor="w").pack(fill="x")
    Label(info_frame, text="Instituição: Chaos Bank S.A.", bg="white", anchor="w").pack(fill="x", pady=(0, 10))

    Label(info_frame, text="Destino", font=("Arial", 11, "bold"), bg="white", anchor="w").pack(fill="x")
    if isinstance(destino_info, str) and len(destino_info) == 11 and destino_info.isdigit():
        usuario_destino = database.get_usuario(destino_info)
        if usuario_destino:
            Label(info_frame, text=f"Nome: {usuario_destino[1]}", bg="white", anchor="w").pack(fill="x")
            Label(info_frame, text=f"CPF: {mask_cpf(destino_info)}", bg="white", anchor="w").pack(fill="x")
    else:
        Label(info_frame, text=f"Chave: {destino_info}", bg="white", anchor="w").pack(fill="x")
    Label(info_frame, text="Instituição: Chaos Bank S.A.", bg="white", anchor="w").pack(fill="x")

    Label(comprovante_window, text=f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", font=("Arial", 8), bg="white").pack(pady=10)
    Button(comprovante_window, text="Fechar", command=comprovante_window.destroy, bg="grey", fg="white").pack(pady=5)