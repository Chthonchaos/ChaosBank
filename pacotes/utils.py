# Arquivo: utils.py


#Biblioteca e Módulos
import hashlib
import smtplib
import ssl
from tkinter import Toplevel, Frame, Label, Button, messagebox
from datetime import datetime
from pacotes import database
from pacotes.config import EMAIL_SENDER, EMAIL_PASSWORD

def hash_senha(senha):
    "Gera um hash  para a senha."
    return hashlib.sha256(senha.encode()).hexdigest()

def mask_cpf(cpf):
    "Esconde o CPF."
    if isinstance(cpf, str) and len(cpf) == 11 and cpf.isdigit():
        return f"{cpf[:3]}.XXX.XXX-{cpf[9:]}"
    return cpf

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

def send_recovery_email(dest_email, nome_cliente, recovery_code):
    "Envia um e-mail de recuperação de senha usando as credenciais do config."
    assunto = "Comunicado Importante: Sua Recuperação de Acesso no ChaosBank"
    corpo_template = f"""Prezado(a) {nome_cliente},

Esperamos que este e-mail o(a) encontre bem.

Nós, do ChaosBank, estamos entrando em contato para fornecer o código de validação para sua recente solicitação de recuperação de senha.

Sua segurança e a eficiência dos nossos serviços são nossa prioridade. Para prosseguir com a criação de uma nova senha, utilize o código exclusivo fornecido abaixo.

Seu Código ChaosBank:

{recovery_code}

Instruções:

Por favor, utilize este código no campo indicado em nosso aplicativo dentro dos próximos 15 minutos.

Atenciosamente,
Equipe ChaosBank
"""
    message = f"Subject: {assunto}\n\n{corpo_template}"
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, dest_email, message.encode('utf-8'))
        return True
    except Exception as e:
        print(f"ERRO AO ENVIAR E-MAIL: {e}")
        messagebox.showerror("Erro de Envio", "Não foi possível enviar o e-mail de recuperação.")
        return False