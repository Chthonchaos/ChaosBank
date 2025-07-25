#Arquivo: database.py
#Banco de dados

#Bibliotecas e Módulos
import sqlite3
from pacotes import config


conn = sqlite3.connect(config.DB_NAME)
c = conn.cursor()

# Função para configurar o banco de dados e criar as tabelas necessárias
def setup_database():

    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        cpf TEXT PRIMARY KEY, nome TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL, saldo REAL DEFAULT 0.0, recovery_code TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS extrato (
        id INTEGER PRIMARY KEY AUTOINCREMENT, cpf TEXT, tipo TEXT, valor REAL,
        descricao TEXT, data DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(cpf) REFERENCES usuarios(cpf)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS emprestimos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, cpf TEXT, valor_emprestado REAL,
        valor_total_a_pagar REAL, valor_pago REAL DEFAULT 0.0, parcelas_totais INTEGER,
        parcelas_pagas INTEGER DEFAULT 0, valor_parcela REAL, status TEXT DEFAULT 'ATIVO',
        FOREIGN KEY(cpf) REFERENCES usuarios(cpf)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS chaves_pix (
        chave TEXT PRIMARY KEY, tipo TEXT, cpf TEXT, FOREIGN KEY(cpf) REFERENCES usuarios(cpf)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS cartoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, cpf TEXT, numero TEXT UNIQUE,
        validade TEXT, cvv TEXT, tipo TEXT, limite REAL, FOREIGN KEY(cpf) REFERENCES usuarios(cpf)
    )''')
    conn.commit()

# Funções de Manipulação de Dados
def get_usuario(cpf):
    """Busca um usuário pelo CPF."""
    c.execute("SELECT * FROM usuarios WHERE cpf = ?", (cpf,))
    return c.fetchone()


#Função para buscar usuário por email
def get_usuario_por_email(email):
    """Busca um usuário pelo email."""
    c.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    c.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    return c.fetchone()


#Função para pegar dados do usuario com base em: Cpf
def get_extrato(cpf):

    c.execute("SELECT tipo, valor, descricao, data FROM extrato WHERE cpf = ? ORDER BY data DESC", (cpf,))
    return c.fetchall()

# Função para pegar emprestimos ativos de um usuario
def get_emprestimos_ativos(cpf):

    c.execute("SELECT id, valor_total_a_pagar, valor_pago, parcelas_totais, parcelas_pagas FROM emprestimos WHERE cpf = ? AND status = 'ATIVO'", (cpf,))
    return c.fetchall()

# Função para pegar emprestimos pagos de um usuario  
def get_emprestimo_por_id(pagamento):

    c.execute("SELECT * FROM emprestimos WHERE id = ?", (pagamento,))
    return c.fetchone()

# Função para registrar uma ação no extrato do usuário
def registrar_acao(cpf, tipo, valor, descricao):

    c.execute("INSERT INTO extrato (cpf, tipo, valor, descricao) VALUES (?, ?, ?, ?)", (cpf, tipo, valor, descricao))
    conn.commit()

# Função para atualizar o saldo do usuário
def atualizar_saldo(cpf, valor_a_somar):

    c.execute("UPDATE usuarios SET saldo = saldo + ? WHERE cpf = ?", (valor_a_somar, cpf))
    conn.commit()

# Função para registrar um novo usuário
def registrar_novo_usuario(cpf, nome, email, senha_hash):

    c.execute("INSERT INTO usuarios (cpf, nome, email, senha) VALUES (?, ?, ?, ?)", (cpf, nome, email, senha_hash))
    conn.commit()

# Função para registrar emprestimos de cada usuario
def registrar_emprestimo(cpf, valor, total_a_pagar, parcelas, valor_parcela):

    c.execute("INSERT INTO emprestimos (cpf, valor_emprestado, valor_total_a_pagar, parcelas_totais, valor_parcela) VALUES (?, ?, ?, ?, ?)",
              (cpf, valor, total_a_pagar, parcelas, valor_parcela))
    conn.commit()

# Função para atualizar o status do emprestimo
def atualizar_emprestimo_pago(pagamento, valor_pago):

    c.execute("UPDATE emprestimos SET valor_pago = valor_pago + ?, parcelas_pagas = parcelas_pagas + 1 WHERE id = ?", (valor_pago, pagamento))
    conn.commit()

# Função para quitar um emprestimo
def quitar_emprestimo(pagamento):

    c.execute("UPDATE emprestimos SET valor_pago = valor_total_a_pagar, parcelas_pagas = parcelas_totais, status = 'QUITADO' WHERE id = ?", (pagamento,))
    conn.commit()

#  Função para verificar se o usuário já está cadastrado 
def salvar_codigo_recuperacao(email, code):

    c.execute("UPDATE usuarios SET recovery_code = ? WHERE email = ?", (code, email))
    conn.commit()

# Função para verificar se o código de recuperação é válido
def verificar_codigo_recuperacao(email, code):

    c.execute("SELECT cpf FROM usuarios WHERE email = ? AND recovery_code = ?", (email, code))
    return c.fetchone() is not None


# Função para redefinir a senha do usuário
def redefinir_senha(email, senha_hash):

    c.execute("UPDATE usuarios SET senha = ?, recovery_code = NULL WHERE email = ?", (senha_hash, email))
    conn.commit()

# Função para buscar os cartões de um usuário
def get_cartoes(cpf):
    c.execute("SELECT numero, validade, cvv, tipo, limite FROM cartoes WHERE cpf = ?", (cpf,))
    return c.fetchall()

# Função para buscar o CPF associado a uma chave Pix
def get_pix_destino(chave):
    c.execute("SELECT cpf FROM chaves_pix WHERE chave = ?", (chave,))
    return c.fetchone()
    
# Função para buscar todas as chaves Pix de um usuário
def get_chaves_pix(cpf):
    c.execute("SELECT chave, tipo FROM chaves_pix WHERE cpf = ?", (cpf,))
    return c.fetchall()

# Função para verificar se uma chave Pix já existe
def check_chave_pix_exists(chave):
    c.execute("SELECT chave FROM chaves_pix WHERE chave = ?", (chave,))
    return c.fetchone() is not None
    
# Função para adicionar uma nova chave Pix
def adicionar_chave_pix(chave, tipo, cpf):
    c.execute("INSERT INTO chaves_pix (chave, tipo, cpf) VALUES (?, ?, ?)", (chave, tipo, cpf))
    conn.commit()

# Função para registrar um novo cartão
def registrar_cartao(cpf, numero, validade, cvv, tipo, limite):
    c.execute("INSERT INTO cartoes (cpf, numero, validade, cvv, tipo, limite) VALUES (?, ?, ?, ?, ?, ?)",
              (cpf, numero, validade, cvv, tipo, limite))
    conn.commit()

# Função para fechar a conexão com o banco de dados
def close_connection():
    conn.close()