# Importando as bibliotecas
import mysql.connector
import bcrypt
import sys
import csv
import matplotlib.pyplot as plt
from flask import Flask
import re

# -------------------------------------------------------------------------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = "chave_super_secreta" 

# Função para conectar ao banco
def criar_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",         
        password="aang_Zuko2", 
        database="gerenciamento_notas_db"
    )

# Medidas de segurança
# Função que obriga a preencher o campo 
def inserirValorObrigatio(prompt):
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        else:
            print("Esse campo necessariamente precisa ser preenchido")

# Função para gerar o hash
def gerar_hash_senha(senha_plana):
    hashed = bcrypt.hashpw(senha_plana.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def checar_senha(senha_plana, hash_armazenado):
    try:
        if isinstance(hash_armazenado, str):
            hash_bytes = hash_armazenado.encode('utf-8')
        else:
            hash_bytes = hash_armazenado
        return bcrypt.checkpw(senha_plana.encode('utf-8'), hash_bytes)
    except Exception as e:
        print("Erro ao checar senha:", e)
        return False

# Senha Forte
def verificar_forca_senha(senha):
    """
    Retorna True se a senha for forte, False se for fraca.
    Critérios:
    - Mínimo de 8 caracteres
    - Pelo menos uma letra maiúscula
    - Pelo menos uma letra minúscula
    - Pelo menos um número
    - Pelo menos um caractere especial
    """
    if len(senha) < 8:
        print("Senha muito curta (mínimo 8 caracteres).")
        return False
    if not re.search(r"[A-Z]", senha):
        print("A senha precisa conter pelo menos uma letra MAIÚSCULA.")
        return False
    if not re.search(r"[a-z]", senha):
        print("A senha precisa conter pelo menos uma letra minúscula.")
        return False
    if not re.search(r"[0-9]", senha):
        print("A senha precisa conter pelo menos um número.")
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        print("A senha precisa conter pelo menos um caractere especial.")
        return False
    print("Senha forte cadastrada!")
    return True

# -------------------------------------------------------------------------------------------------------------------------------------------

# CRUD USUARIO
# CREATE
def criar_usuario():
    print(f"\n {' Criar Usuário ':-^50} ")
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()
    cpf = input("CPF (opcional): ").strip() or None
    tipo = input("Tipo (aluno/professor/coordenador/administrador): ").strip().lower()
    if tipo not in ('aluno','professor','coordenador','administrador'):
        print("Tipo inválido. Você será cadastrado como aluno.")
        tipo = 'aluno'
    while True:
        senha = input("Senha: ").strip()
        if verificar_forca_senha(senha):
            break

    hash_senha = gerar_hash_senha(senha)
    ativo = 1
    conn = None
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = ("INSERT INTO Usuarios (nome, email, cpf, senha, tipo_usuario, ativo) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (nome, email, cpf, hash_senha, tipo, ativo))
        conn.commit()
        print("Usuário criado com id:", cursor.lastrowid)
    except mysql.connector.Error as err:
        print("Erro ao criar usuário:", err)
    finally:
        if conn:
            conn.close()

# READE
def listar_usuarios():
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nome, email, cpf, tipo_usuario, ativo FROM Usuarios")
        rows = cursor.fetchall()
        print(f"\n {'Criar Usuário':^-60} ")
        for r in rows:
            print(f"ID:{r[0]:<3} Nome:{r[1]:<20} Email:{r[2]:<30} Tipo:{r[4]:<12} Ativo:{bool(r[5])}")
    except Exception as e:
        print("Erro ao listar usuários:", e)
    finally:
        if conn:
            conn.close()

# UPDATE
def editar_usuario():
    listar_usuarios()
    try:
        idu = int(input("Digite o ID do usuário a editar: "))
    except ValueError:
        print("ID inválido.")
        return
    nome = input("Novo nome (vazio para manter): ").strip()
    email = input("Novo email (vazio para manter): ").strip()
    cpf = input("Novo CPF (vazio para manter): ").strip()
    tipo = input("Novo tipo (aluno/professor/coordenador/administrador) (vazio para manter): ").strip().lower()
    ativo_in = input("Ativo? (s/n) (vazio para manter): ").strip().lower()

    try:
        conn = criar_conexao()
        cursor = conn.cursor()

        # buscar dados atuais
        cursor.execute("SELECT nome, email, cpf, tipo_usuario, ativo FROM Usuarios WHERE id_usuario=%s", (idu,))
        row = cursor.fetchone()
        if not row:
            print("Usuário não encontrado.")
            return
        nome_atual, email_atual, cpf_atual, tipo_atual, ativo_atual = row

        nome_final = nome if nome else nome_atual
        email_final = email if email else email_atual
        cpf_final = cpf if cpf else cpf_atual
        tipo_final = tipo if tipo in ('aluno','professor','coordenador','administrador') else tipo_atual
        if ativo_in == 's':
            ativo_final = 1
        elif ativo_in == 'n':
            ativo_final = 0
        else:
            ativo_final = ativo_atual

        cursor.execute(
            "UPDATE Usuarios SET nome=%s, email=%s, cpf=%s, tipo_usuario=%s, ativo=%s WHERE id_usuario=%s",
            (nome_final, email_final, cpf_final, tipo_final, ativo_final, idu)
        )
        conn.commit()
        print("Usuário atualizado.")
    except Exception as e:
        print("Erro ao editar usuário:", e)
    finally:
        if conn:
            conn.close()

# DELETE
def remover_usuario():
    listar_usuarios()
    try:
        idu = int(input("Digite o ID do usuário a remover: "))
    except ValueError:
        print("ID inválido.")
        return
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario=%s", (idu,))
        conn.commit()
        if cursor.rowcount > 0:
            print("Usuário removido.")
        else:
            print("Usuário não encontrado.")
    except Exception as e:
        print("Erro ao remover usuário:", e)
    finally:
        if conn:
            conn.close()

def autenticar():
    print("\n--- Login ---")
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nome, email, senha, tipo_usuario, ativo FROM Usuarios WHERE email=%s", (email, senha))
        row = cursor.fetchone()
        if not row:
            print("Informações inválidas.")
            return None
        id_usuario, nome, email_db, hash_armazenado, tipo_usuario, ativo = row
        if not ativo:
            print("Usuário inativo.")
            return None
        if checar_senha(senha, hash_armazenado):
            print(f"Autenticado como {nome} ({tipo_usuario})")
            # retornar um dicionário simples com dados do usuário
            return {"id_usuario": id_usuario, "nome": nome, "email": email_db, "tipo": tipo_usuario}
        else:
            print("Informações inválidas.")
            return None
    except Exception as e:
        print("Erro ao autenticar:", e)
        return None
    finally:
        if conn:
            conn.close()

# -------------------------------------------------------------------------------------------------------------------------------------------

# CRUD NOTAS
def calcular_media_simples(n1, n2, n3, recuperacao):
    notas = []
    if n1 is not None:
        notas.append(n1)
    if n2 is not None:
        notas.append(n2)
    if n3 is not None:
        notas.append(n3)
    if not notas and recuperacao is None:
        return None
    media = (sum(notas)/len(notas)) if notas else 0.0
    if recuperacao is not None:
        media = max(media, recuperacao)
    return round(media, 2)

# CREATE/UPDATE DE NOTAS
def lancar_ou_atualizar_nota():
    print("\n--- Lançar / Atualizar Nota ---")
    try:
        id_aluno = int(input("ID do aluno: "))
        id_materia = int(input("ID da matéria: "))
    except ValueError:
        print("IDs devem ser números inteiros.")
        return
    # procurar se já existe nota para esse aluno+materia
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT id_nota, nota1, nota2, nota3, recuperacao, nota_final, id_professor, ano_letivo "
                       "FROM Notas WHERE id_aluno=%s AND id_materia=%s", (id_aluno, id_materia))
        row = cursor.fetchone()

        if row:
            print("Já existe registro de nota encontrado. Iremos atualizar.")
            id_nota = row[0]
            print("Notas atuais:", row[1], row[2], row[3], "Rec:", row[4], "Final:", row[5])
        else:
            id_nota = None

        def ler_float_permitido(prompt):
            v = input(prompt + " (vazio para None): ").strip()
            return float(v) if v != "" else None

        nota1 = ler_float_permitido("Nota 1")
        nota2 = ler_float_permitido("Nota 2")
        nota3 = ler_float_permitido("Nota 3")
        rec = ler_float_permitido("Recuperação")
        ano = input("Ano letivo (ex: 2025): ").strip()
        ano = int(ano) if ano else None
        id_prof = input("ID do professor (inteiro): ").strip()
        id_prof = int(id_prof) if id_prof else None

        nota_final = calcular_media_simples(nota1, nota2, nota3, rec)

        if id_nota:
            sql = ("UPDATE Notas SET nota1=%s, nota2=%s, nota3=%s, recuperacao=%s, nota_final=%s, id_professor=%s, ano_letivo=%s "
                   "WHERE id_nota=%s")
            cursor.execute(sql, (nota1, nota2, nota3, rec, nota_final, id_prof, ano, id_nota))
            conn.commit()
            print("Nota atualizada.")
        else:
            sql = ("INSERT INTO Notas (id_aluno, id_materia, id_professor, nota1, nota2, nota3, recuperacao, nota_final, ano_letivo) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            cursor.execute(sql, (id_aluno, id_materia, id_prof, nota1, nota2, nota3, rec, nota_final, ano))
            conn.commit()
            print("Nota inserida com id:", cursor.lastrowid)
    except Exception as e:
        print("Erro ao inserir/atualizar nota:", e)
    finally:
        if conn:
            conn.close()

# READE 
def listar_notas_por_aluno():
    try:
        id_aluno = int(input("ID do aluno para listar notas: "))
    except ValueError:
        print("ID inválido.")
        return
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT id_nota, id_materia, id_professor, nota1, nota2, nota3, recuperacao, nota_final, ano_letivo "
                       "FROM Notas WHERE id_aluno=%s", (id_aluno,))
        rows = cursor.fetchall()
        if not rows:
            print("Nenhuma nota encontrada para esse aluno.")
            return
        print(f"\n--- Notas do Aluno {id_aluno} ---")
        for r in rows:
            print(f"NotaID:{r[0]:<3} Mat:{r[1]:<3} Prof:{r[2]:<3} N1:{r[3]} N2:{r[4]} N3:{r[5]} Rec:{r[6]} Final:{r[7]} Ano:{r[8]}")
    except Exception as e:
        print("Erro ao listar notas:", e)
    finally:
        if conn:
            conn.close()

def listar_todas_notas():
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT id_nota, id_aluno, id_materia, id_professor, nota1, nota2, nota3, recuperacao, nota_final, ano_letivo FROM Notas")
        rows = cursor.fetchall()
        if not rows:
            print("Sem notas registradas.")
            return []
        print("\n--- Todas as Notas ---")
        for r in rows:
            print(f"ID:{r[0]:<3} Aluno:{r[1]:<3} Mat:{r[2]:<3} Prof:{r[3]:<3} N1:{r[4]} N2:{r[5]} N3:{r[6]} Rec:{r[7]} Final:{r[8]} Ano:{r[9]}")
        return rows
    except Exception as e:
        print("Erro ao listar todas as notas:", e)
        return []
    finally:
        if conn:
            conn.close()
# -----------------------------------------------------------------------------------------------------------------------------------------------

# CRIANDO RELATÓRIO
def exportar_csv_notas():
    rows = listar_todas_notas()
    if not rows:
        return
    fname = input("Nome do arquivo CSV: ").strip() or "relatorio_notas.csv"
    try:
        with open(fname, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["id_nota","id_aluno","id_materia","id_professor","nota1","nota2","nota3","recuperacao","nota_final","ano_letivo"])
            for r in rows:
                writer.writerow(r)
        print("Exportado para", fname)
    except Exception as e:
        print("Erro ao exportar CSV:", e)

def grafico_media_por_aluno():
    rows = listar_todas_notas()
    if not rows:
        return
    soma = {}
    cont = {}
    for r in rows:
        id_aluno = r[1]
        nota_final = r[8]
        # se nota_final for None, tentar calcular com as colunas
        if nota_final is None:
            n1, n2, n3, rec = r[4], r[5], r[6], r[7]
            nota_final = calcular_media_simples(n1, n2, n3, rec) or 0.0
        soma[id_aluno] = soma.get(id_aluno, 0.0) + float(nota_final)
        cont[id_aluno] = cont.get(id_aluno, 0) + 1
    alunos = sorted(soma.keys())
    medias = [round(soma[a]/cont[a], 2) for a in alunos]
    plt.figure()
    plt.bar([str(a) for a in alunos], medias)
    plt.title("Média por aluno")
    plt.xlabel("ID Aluno")
    plt.ylabel("Média")
    plt.tight_layout()
    print("Mostrando gráfico. Feche a janela para continuar.")
    plt.show()

# ------------------------------------------------------------------------------------------------------------------------------------------------
import sys

# CRIANDO O CATALOGO DE OPÇÕES
def catalogo():
    print(f'-' * 45)
    print(f'|{"Sistema de Gerenciamento de Notas":^43}|')
    print(f'-' * 45)
    print(f'|{" 1 - Login":<43}|')
    print(f'|{" 2 - Criar Usuário":<43}|')
    print(f'|{" 0 - Sair":<43}|')
    print(f'-' * 45)

    escolha = input("Digite uma opção: ").strip()
    return escolha

# catalogo do administradores
def catalogo_admin():
    print(f'=' * 45)
    print(f'|{" Painel do Administrador ":=^43}|')
    print(f'=' * 45)
    print(f'|{" 1 - Listar Usuários":<43}|')
    print(f'|{" 2 - Criar Usuário":<43}|')
    print(f'|{" 3 - Editar Usuário":<43}|')
    print(f'|{" 4 - Remover Usuário":<43}|')
    print(f'|{" 5 - Lançar/Atualizar Notas":<43}|')
    print(f'|{" 6 - Listar Todas as Notas":<43}|')
    print(f'|{" 7 - Exportar Notas (CSV)":<43}|')
    print(f'|{" 8 - Gráfico de Média por Aluno":<43}|')
    print(f'|{" 0 - Logout":<43}|')
    print(f'=' * 45)

    escolha = input("Digite uma opção: ").strip()
    return escolha


# catalogo dos professores
def catalogo_professor():
    print(f'=' * 45)
    print(f'|{" Painel do Professor ":=^43}|')
    print(f'=' * 45)
    print(f'|{" 1 - Lançar/Atualizar Nota":<43}|')
    print(f'|{" 2 - Listar Notas por Aluno":<43}|')
    print(f'|{" 0 - Logout":<43}|')
    print(f'=' * 45)

    escolha = input("Digite uma opção: ").strip()
    return escolha


# catalogo dos alunos
def catalogo_aluno():
    print(f'=' * 45)
    print(f'|{" Painel do Aluno ":=^43}|')
    print(f'=' * 45)
    print(f'|{" 1 - Ver Minhas Notas":<43}|')
    print(f'|{" 0 - Logout":<43}|')
    print(f'=' * 45)

    escolha = input("Digite uma opção: ").strip()
    return escolha


def main():
    while True:
        escolha = catalogo()

        if escolha == "0":
            print("Encerrando o sistema...")
            sys.exit(0)

        elif escolha == "1":
            user = autenticar()
            if not user:
                continue

            tipo = user['tipo']
            if tipo == 'administrador':
                while True:
                    e = catalogo_admin()
                    if e == "0":
                        break
                    elif e == "1":
                        listar_usuarios()
                    elif e == "2":
                        criar_usuario()
                    elif e == "3":
                        editar_usuario()
                    elif e == "4":
                        remover_usuario()
                    elif e == "5":
                        lancar_ou_atualizar_nota()
                    elif e == "6":
                        listar_todas_notas()
                    elif e == "7":
                        exportar_csv_notas()
                    elif e == "8":
                        grafico_media_por_aluno()
                    else:
                        print("Opção inválida. Tente novamente.")

            elif tipo == 'professor':
                while True:
                    e = catalogo_professor()
                    if e == "0":
                        break
                    elif e == "1":
                        lancar_ou_atualizar_nota()
                    elif e == "2":
                        listar_notas_por_aluno()
                    else:
                        print("Opção inválida. Tente novamente.")

            elif tipo == 'aluno':
                while True:
                    e = catalogo_aluno()
                    if e == "0":
                        break
                    elif e == "1":
                        listar_notas_por_aluno()
                    else:
                        print("Opção inválida. Tente novamente.")
            else:
                print("Tipo de usuário não reconhecido.")

        elif escolha == "2":
            criar_usuario()

        else:
            print("Opção inválida. Digite apenas números válidos.")


if __name__ == "__main__":
    main()
