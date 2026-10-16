import sqlite3
import hashlib

# 1. Conecta ao Banco de Dados (ele cria o arquivo 'senhas.db' sozinho)
conexao = sqlite3.connect("senhas.db")
cursor = conexao.cursor()

# 2. Cria a tabela para guardar os dados com segurança
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cofres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        servico TEXT NOT NULL,
        usuario TEXT NOT NULL,
        senha_criptografada TEXT NOT NULL
    )
""")
conexao.commit()

def cadastrar_senha():
    servico = input("Qual o nome do serviço/site (ex: Netflix, Email): ")
    usuario = input("Qual o seu usuário ou e-mail: ")
    senha_plana = input("Qual a senha: ")
    
    # [SEGURANÇA] Criptografando a senha usando SHA-256 para não salvar texto puro
    senha_cripto = hashlib.sha256(senha_plana.encode()).hexdigest()
    
    # [BANCO DE DADOS] Inserindo os dados na tabela SQL
    cursor.execute("""
        INSERT INTO cofres (servico, usuario, senha_criptografada) 
        VALUES (?, ?, ?)
    """, (servico, usuario, senha_cripto))
    
    conexao.commit()
    print(f"\n[Sucesso] Senha para o serviço '{servico}' salva e criptografada com segurança!")

def listar_senhas():
    cursor.execute("SELECT servico, usuario, senha_criptografada FROM cofres")
    registros = cursor.fetchall()
    
    print("\n--- SEU COFRE DE SENHAS ---")
    if not registros:
        print("Nenhuma senha cadastrada ainda.")
    for reg in registros:
        print(f"Serviço: {reg[0]} | Usuário: {reg[1]} | Senha (Hash): {reg[2][:15]}...")

# Menu interativo simples
while True:
    print("\n1. Cadastrar nova senha")
    print("2. Ver senhas salvas")
    print("3. Sair")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1":
        cadastrar_senha()
    elif opcao == "2":
        listar_senhas()
    elif opcao == "3":
        print("Saindo do cofre... Até logo!")
        conexao.close()
        break
    else:
        print("Opção inválida, tente de novo.")
