#Módulos
from .database import (
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
from .utils import (
    hash_senha,
    mask_cpf,
    gerar_comprovante,
)  

__all__ = [
    "setup_database",
    "get_usuario",
    "get_usuario_por_email",
    "get_extrato",
    "get_emprestimos_ativos",
    "get_emprestimo_por_id",
    "registrar_acao",
    "atualizar_saldo",
    "registrar_novo_usuario",
    "registrar_emprestimo",
    "atualizar_emprestimo_pago",
    "quitar_emprestimo",
    "salvar_codigo_recuperacao",
    "verificar_codigo_recuperacao",
    "redefinir_senha",
    "close_connection",
    "hash_senha",
    "mask_cpf",
    "gerar_comprovante",
    "send_recovery_email"
]