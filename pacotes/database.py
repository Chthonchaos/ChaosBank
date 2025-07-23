#Arquivo: database.py
#Banco de dados

#Bibliotecas e Módulos
import sqlite3
from pacotes import config


conn = sqlite3.connect(config.DB_NAME)
c = conn.cursor()

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
    conn.commit()


def get_usuario(cpf):

    c.execute("SELECT * FROM usuarios WHERE cpf = ?", (cpf,))
    return c.fetchone()

def get_usuario_por_email(email):

    c.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    return c.fetchone()
    
def get_extrato(cpf):

    c.execute("SELECT tipo, valor, descricao, data FROM extrato WHERE cpf = ? ORDER BY data DESC", (cpf,))
    return c.fetchall()

def get_emprestimos_ativos(cpf):

    c.execute("SELECT id, valor_total_a_pagar, valor_pago, parcelas_totais, parcelas_pagas FROM emprestimos WHERE cpf = ? AND status = 'ATIVO'", (cpf,))
    return c.fetchall()
    
def get_emprestimo_por_id(pagamento):

    c.execute("SELECT * FROM emprestimos WHERE id = ?", (pagamento,))
    return c.fetchone()

def registrar_acao(cpf, tipo, valor, descricao):

    c.execute("INSERT INTO extrato (cpf, tipo, valor, descricao) VALUES (?, ?, ?, ?)", (cpf, tipo, valor, descricao))
    conn.commit()

def atualizar_saldo(cpf, valor_a_somar):

    c.execute("UPDATE usuarios SET saldo = saldo + ? WHERE cpf = ?", (valor_a_somar, cpf))
    conn.commit()

def registrar_novo_usuario(cpf, nome, email, senha_hash):

    c.execute("INSERT INTO usuarios (cpf, nome, email, senha) VALUES (?, ?, ?, ?)", (cpf, nome, email, senha_hash))
    conn.commit()

def registrar_emprestimo(cpf, valor, total_a_pagar, parcelas, valor_parcela):

    c.execute("INSERT INTO emprestimos (cpf, valor_emprestado, valor_total_a_pagar, parcelas_totais, valor_parcela) VALUES (?, ?, ?, ?, ?)",
              (cpf, valor, total_a_pagar, parcelas, valor_parcela))
    conn.commit()
    
def atualizar_emprestimo_pago(pagamento, valor_pago):

    c.execute("UPDATE emprestimos SET valor_pago = valor_pago + ?, parcelas_pagas = parcelas_pagas + 1 WHERE id = ?", (valor_pago, pagamento))
    conn.commit()

def quitar_emprestimo(pagamento):

    c.execute("UPDATE emprestimos SET valor_pago = valor_total_a_pagar, parcelas_pagas = parcelas_totais, status = 'QUITADO' WHERE id = ?", (pagamento,))
    conn.commit()
    
def salvar_codigo_recuperacao(email, code):

    c.execute("UPDATE usuarios SET recovery_code = ? WHERE email = ?", (code, email))
    conn.commit()

def verificar_codigo_recuperacao(email, code):

    c.execute("SELECT cpf FROM usuarios WHERE email = ? AND recovery_code = ?", (email, code))
    return c.fetchone() is not None

def redefinir_senha(email, senha_hash):

    c.execute("UPDATE usuarios SET senha = ?, recovery_code = NULL WHERE email = ?", (senha_hash, email))
    conn.commit()

def close_connection():
    conn.close()