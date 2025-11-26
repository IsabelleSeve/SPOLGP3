# Importando as bibliotecas
import mysql.connector
import bcrypt
import sys
import csv
import matplotlib.pyplot as plt
from flask import Flask
import re

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

# Função para verificar se a senha inserida é a mesma registrada no banco
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

# Faz a validação das informações para o login
def autenticar():
    print(f"\n{' Login ':-^75}")
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()

    try:
        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id_usuario, nome, email, senha, tipo_usuario, ativo FROM Usuarios WHERE email=%s",
            (email,)
        )
        row = cursor.fetchone()

        if not row:
            print("Email não encontrado.")
            return None

        if not row["ativo"]:
            print("Usuário inativo.")
            return None

        if checar_senha(senha, row["senha"]):
            print(f"Autenticado como {row['nome']} ({row['tipo_usuario']})")
            return {
                "id_usuario": row["id_usuario"],
                "nome": row["nome"],
                "email": row["email"],
                "tipo": row["tipo_usuario"]
            }
        else:
            print("Senha incorreta.")
            return None

    except Exception as e:
        print("Erro ao autenticar:", e)
        return None
    finally:
        if conn:
            conn.close()


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


# LISTAR AUXILIARES
def listar_alunos():
    try:
        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT a.id_aluno, u.nome, u.email, u.ativo
            FROM Alunos a
            JOIN Usuarios u ON a.id_usuario = u.id_usuario
            ORDER BY a.id_aluno
        """)

        rows = cursor.fetchall()

        print(f"\n {'Lista de Alunos':-75} ")
        print(f"{'ID_Aluno':<10} {'Nome':<25} {'Email':<30} {'Ativo':<6}")
        print('-' * 75)

        if not rows:
            print("Nenhum aluno encontrado.")
            return []

        for r in rows:
            ativo_formatado = "Sim" if r["ativo"] == 1 else "Não"
            print(f"{r['id_aluno']:<10} {r['nome']:<25} {r['email']:<30} {ativo_formatado:<6}")

        return rows

    except Exception as e:
        print("Erro ao listar alunos:", e)
        return []

    finally:
        if conn:
            conn.close()

def listar_professores():
    try:
        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT p.id_professor, u.nome, u.email, p.formacao, u.ativo
            FROM Professores p
            JOIN Usuarios u ON p.id_usuario = u.id_usuario
        """)

        rows = cursor.fetchall()

        print(f"\n{' Lista de Professores ':-^93}")
        print(f"{'ID_Prof':<10} {'Nome':<25} {'Email':<30} {'Formação':<20} {'Ativo':<6}")
        print('-' * 95)

        for r in rows:
            print(f"{r['id_professor']:<10} {r['nome']:<25} {r['email']:<30} {r['formacao'] or '---':<20} {str(bool(r['ativo'])):<6}")

        return rows

    except Exception as e:
        print("Erro ao listar professores:", e)
        return []
    finally:
        if conn:
            conn.close()

def listar_materias():
    try:
        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_materia, nome_materia, carga_horaria, descricao FROM Materias")

        rows = cursor.fetchall()

        print(f"\n{' Lista de Materias ':-^93}")
        print(f"{'ID_Mat':<10} {'Nome da Matéria':<30} {'Carga Horária':<15} {'Descrição':<30}")
        print('-' * 95)

        for r in rows:
            descricao = (r['descricao'][:25] + "...") if r['descricao'] and len(r['descricao']) > 25 else (r['descricao'] or "")
            print(f"{r['id_materia']:<10} {r['nome_materia']:<30} {str(r['carga_horaria'])+'h':<15} {descricao:<30}")

        return rows

    except Exception as e:
        print("Erro ao listar matérias:", e)
        return []
    finally:
        if conn:
            conn.close()

def listar_turmas():
    try:
        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_turma, nome_turma, ano_letivo, turno FROM Turmas")

        rows = cursor.fetchall()

        print(f"\n{' Lista de Turmas ':-^93}")
        print(f"{'ID_Turma':<10} {'Nome da Turma':<20} {'Ano':<10} {'Turno':<15}")
        print('-' * 60)

        for r in rows:
            print(f"{r['id_turma']:<10} {r['nome_turma']:<20} {str(r['ano_letivo']):<10} {r['turno']:<15}")

        return rows

    except Exception as e:
        print("Erro ao listar turmas:", e)
        return []
    finally:
        if conn:
            conn.close()


# USUARIO
# CREATE USUÁRIO
def criar_usuario():
    print(f"\n{' Criar Usuário ':-^75}")
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()
    cpf = input("CPF (opcional): ").strip() or None
    tipo = input("Tipo (aluno/professor/coordenador/administrador): ").strip().lower()

    if tipo not in ('aluno', 'professor', 'coordenador', 'administrador'):
        print("Tipo inválido. O usuário será cadastrado como aluno.")
        tipo = 'aluno'

    # SENHA
    while True:
        senha = input("Senha: ").strip()
        if verificar_forca_senha(senha):
            break

    hash_senha = gerar_hash_senha(senha)
    ativo = 1

    try:
        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)

        sql = ("INSERT INTO Usuarios (nome, email, cpf, senha, tipo_usuario, ativo) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (nome, email, cpf, hash_senha, tipo, ativo))
        conn.commit()

        id_usuario = cursor.lastrowid
        print("Usuário criado com ID:", id_usuario)

        # SE FOR ALUNO
        if tipo == "aluno":
            print("\n--- Informações adicionais de ALUNO ---")
            listar_turmas()

            id_turma = input("Digite o ID da turma para o aluno: ").strip()

            cursor.execute("SELECT id_aluno FROM Alunos WHERE id_usuario=%s", (id_usuario,))
            aluno = cursor.fetchone()

            if not aluno:
                print("ERRO!!")
                return

            if id_turma.isdigit():
                cursor.execute(
                    "UPDATE Alunos SET id_turma=%s WHERE id_aluno=%s",
                    (int(id_turma), aluno["id_aluno"])
                )
                conn.commit()
                print("Aluno associado à turma com sucesso!")

        # SE FOR PROFESSOR
        elif tipo == "professor":
            print("\n--- Informações adicionais de PROFESSOR ---")
            cursor.execute(
                "SELECT id_professor FROM Professores WHERE id_usuario=%s",
                (id_usuario,)
            )
            prof = cursor.fetchone()

            if not prof:
                print("ERRO!")
                return

            id_professor = prof["id_professor"]
            formacao = input("Digite a formação do professor: ").strip()
            cursor.execute(
                "UPDATE Professores SET formacao=%s WHERE id_professor=%s",
                (formacao, id_professor)
            )
            conn.commit()
            print("Formação cadastrada com sucesso!")

            print("\nMaterias disponíveis:")
            materias = listar_materias()
            ids_sel = input("IDs das matérias que ele leciona: ").strip()

            if ids_sel:
                materias_escolhidas = [
                    int(x) for x in ids_sel.split(",") if x.strip().isdigit()
                ]

                for id_materia in materias_escolhidas:
                    cursor.execute(
                        "INSERT IGNORE INTO Professores_Materias (id_professor, id_materia) VALUES (%s, %s)",
                        (id_professor, id_materia)
                    )
                conn.commit()

                print("Professor associado às matérias com sucesso!")
            else:
                print("Nenhuma matéria selecionada.")

        else:
            print("Nenhuma informação adicional necessária para este tipo de usuário.")

    except mysql.connector.Error as err:
        print("Erro ao criar usuário:", err)

    finally:
        if conn:
            conn.close()


# READ USUÁRIO
def listar_usuarios():
    conn = None
    try:
        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, nome, email, cpf, tipo_usuario, ativo FROM Usuarios")
        rows = cursor.fetchall()

        if not rows:
            print("\nNenhum usuário cadastrado.")
            return []

        print(f"\n{' Lista de Usuários ':-^90}")
        print(f"{'ID':<6} {'Nome':<25} {'Email':<35} {'Tipo':<15} {'Ativo':<6}")
        print('-' * 90)

        for r in rows:
            idu = r.get('id_usuario')
            nome = r.get('nome') or ''
            email = r.get('email') or ''
            tipo = r.get('tipo_usuario') or ''
            ativo = bool(r.get('ativo'))
            print(f"{str(idu):<6} {nome:<25} {email:<35} {tipo:<15} {str(ativo):<6}")

        return rows

    except mysql.connector.Error as err:
        print("Erro ao listar usuários (MySQL):", err)
        return []
    except Exception as e:
        print("Erro ao listar usuários:", e)
        return []
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
        cursor = conn.cursor(dictionary=True)

        # Buscar dados atuais
        cursor.execute("""
            SELECT nome, email, cpf, tipo_usuario, ativo
            FROM Usuarios
            WHERE id_usuario = %s
        """, (idu,))

        row = cursor.fetchone()

        if not row:
            print("Usuário não encontrado.")
            return

        # Como row é um dicionário, acessamos por chave:
        nome_atual = row["nome"]
        email_atual = row["email"]
        cpf_atual = row["cpf"]
        tipo_atual = row["tipo_usuario"]
        ativo_atual = row["ativo"]

        # Manter valores antigos se estiver vazio
        nome_final = nome if nome else nome_atual
        email_final = email if email else email_atual
        cpf_final = cpf if cpf else cpf_atual
        
        if tipo in ('aluno', 'professor', 'coordenador', 'administrador'):
            tipo_final = tipo
        else:
            tipo_final = tipo_atual

        if ativo_in == 's':
            ativo_final = 1
        elif ativo_in == 'n':
            ativo_final = 0
        else:
            ativo_final = ativo_atual

        # Atualizar
        cursor.execute("""
            UPDATE Usuarios
            SET nome=%s,
                email=%s,
                cpf=%s,
                tipo_usuario=%s,
                ativo=%s
            WHERE id_usuario=%s
        """, (nome_final, email_final, cpf_final, tipo_final, ativo_final, idu))

        conn.commit()
        print("Usuário atualizado com sucesso!")

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
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario=%s", (idu,))
        conn.commit()
        if cursor.rowcount > 0:
            print("Usuário removido.")
        else:
            print("Usuário não encontrado.")
    except Exception as e:
        print("Erro ao remover usuário:", e)
        return idu
    finally:
        if conn:
            conn.close()


# NOTAS
# CALCULAR MÉDIA DAS NOTAS
def calcular_media(n1, n2, n3, recuperacao):
    notas = [n for n in (n1, n2, n3) if n is not None]

    if not notas and recuperacao is None:
        return None

    media = sum(notas) / len(notas) if notas else 0

    if recuperacao is not None:
        media = max(media, recuperacao)

    return round(media, 2)

# PROCURAR O ID DO ALUNO PARA USAR COMO BASE DA CONSULTA
def id_aluno_por_usuario(id_usuario):
    try:
        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_aluno FROM Alunos WHERE id_usuario=%s", (id_usuario,))
        row = cursor.fetchone()

        return row["id_aluno"] if row else None

    except Exception:
        return None

    finally:
        if conn:
            conn.close()


def lancar_ou_atualizar_nota():
    listar_alunos()
    print("\n--- Lançar / Atualizar Nota ---")

    try:
        id_aluno = int(input("ID do aluno: "))
        listar_materias()
        id_materia = int(input("ID da matéria: "))

        listar_professores()
        id_professor = int(input("ID do professor responsável: "))

    except ValueError:
        print("IDs devem ser números inteiros.")
        return

    try:
        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_nota, nota1, nota2, nota3, recuperacao, nota_final, ano_letivo
            FROM Notas
            WHERE id_aluno=%s AND id_materia=%s
        """, (id_aluno, id_materia))

        row = cursor.fetchone()

        if row:
            print("\nRegistro encontrado — atualização.")
            id_nota = row["id_nota"]
            print(f"Notas atuais: {row['nota1']}, {row['nota2']}, {row['nota3']} | Rec: {row['recuperacao']} | Final: {row['nota_final']}")
        else:
            id_nota = None

        def ler_float(prompt):
            valor = input(prompt + " (vazio = None): ").strip()
            return float(valor) if valor else None

        nota1 = ler_float("Nota 1")
        nota2 = ler_float("Nota 2")
        nota3 = ler_float("Nota 3")
        rec = ler_float("Recuperação")

        ano = input("Ano letivo (ex: 2025): ").strip()
        ano = int(ano) if ano else None

        nota_final = calcular_media(nota1, nota2, nota3, rec)

        if id_nota:
            cursor.execute("""
                UPDATE Notas 
                SET nota1=%s, nota2=%s, nota3=%s, recuperacao=%s, nota_final=%s, ano_letivo=%s, id_professor=%s
                WHERE id_nota=%s
            """, (nota1, nota2, nota3, rec, nota_final, ano, id_professor, id_nota))
            conn.commit()
            print("\n✔ Nota atualizada com sucesso.")

        else:
            cursor.execute("""
                INSERT INTO Notas 
                    (id_aluno, id_materia, id_professor, nota1, nota2, nota3, recuperacao, nota_final, ano_letivo)
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_aluno, id_materia, id_professor,
                  nota1, nota2, nota3, rec, nota_final, ano))

            conn.commit()
            print("\n✔ Nota inserida com ID:", cursor.lastrowid)

    except Exception as e:
        print("Erro ao lançar/atualizar nota:", e)

    finally:
        if conn:
            conn.close()

           
def listar_notas_por_aluno(id_aluno=None):
    listar_alunos()

    if id_aluno is None:
        try:
            id_aluno = int(input("Digite o ID do aluno: ").strip())
        except ValueError:
            print("ID inválido. Digite apenas números.")
            return

    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT n.id_materia, m.nome_materia, n.nota1, n.nota2, n.nota3, n.recuperacao, n.nota_final
        FROM Notas n
        JOIN Materias m ON n.id_materia = m.id_materia
        WHERE n.id_aluno = %s
    """, (id_aluno,))

    linhas = cursor.fetchall()

    if not linhas:
        print("Nenhuma nota encontrada.")
        conn.close()
        return

    print(f"\nNotas do aluno {id_aluno}:")
    for row in linhas:
        print(row)

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

def listar_notas_do_professor(id_professor=None):
    try:
        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                n.id_nota,
                a.id_aluno,
                u.nome AS nome_aluno,
                m.id_materia,
                m.nome_materia,
                t.id_turma,
                t.nome_turma,
                n.nota1,
                n.nota2,
                n.nota3,
                n.recuperacao,
                n.nota_final,
                n.ano_letivo
            FROM Notas n
            JOIN Alunos a ON a.id_aluno = n.id_aluno
            JOIN Usuarios u ON u.id_usuario = a.id_usuario        
            JOIN Materias m ON m.id_materia = n.id_materia
            JOIN Turmas t ON t.id_turma = a.id_turma              
            WHERE n.id_professor = %s
            ORDER BY t.nome_turma, m.nome_materia, u.nome;
        """, (id_professor,))

        linhas = cursor.fetchall()

        if not linhas:
            print("Nenhuma nota encontrada para este professor.")
            return
        
        print(f"\n{' NOTAS DO PROFESSOR ':-^95}\n")
        turma_atual = None
        materia_atual = None

        for row in linhas:

            if turma_atual != row["nome_turma"]:
                turma_atual = row["nome_turma"]
                print(f"\n=== Turma: {turma_atual} ===")

            if materia_atual != row["nome_materia"]:
                materia_atual = row["nome_materia"]
                print(f"\n--- Matéria: {materia_atual} ---")
                print(f"{'Aluno':<25} {'N1':<5} {'N2':<5} {'N3':<5} {'Rec':<7} {'Final':<6}")

            print(f"{row['nome_aluno']:<25} {str(row['nota1']):<5} {str(row['nota2']):<5} {str(row['nota3']):<5} {str(row['recuperacao']):<7} {str(row['nota_final']):<6}")

    except Exception as e:
        print("Erro ao listar notas do professor:", e)

    finally:
        if conn:
            conn.close()

# RELATÓRIO

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
        if nota_final is None:
            n1, n2, n3, rec = r[4], r[5], r[6], r[7]
            nota_final = calcular_media(n1, n2, n3, rec) or 0.0
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


# CRIANDO CATALOGOS DE OPCOES
def catalogo():
    print(f'-' * 75)
    print(f'|{"Sistema de Gerenciamento de Notas":^73}|')
    print(f'-' * 75)
    print(f'|{" 1 - Login":<73}|')
    print(f'|{" 2 - Criar Usuário":<73}|')
    print(f'|{" 0 - Sair":<73}|')
    print(f'-' * 75)

    escolha = input("Digite uma opção: ").strip()
    return escolha

# catalogo do administradores
def catalogo_admin():
    print(f'=' * 75)
    print(f'|{" Painel do Administrador ":=^73}|')
    print(f'=' * 75)
    print(f'|{" 1 - Listar Usuários":<73}|')
    print(f'|{" 2 - Criar Usuário":<73}|')
    print(f'|{" 3 - Editar Usuário":<73}|')
    print(f'|{" 4 - Remover Usuário":<73}|')
    print(f'|{" 5 - Lançar/Atualizar Notas":<73}|')
    print(f'|{" 6 - Listar Todas as Notas":<73}|')
    print(f'|{" 7 - Exportar Notas (CSV)":<73}|')
    print(f'|{" 8 - Gráfico de Média por Aluno":<73}|')
    print(f'|{" 0 - Logout":<73}|')
    print(f'=' * 75)

    escolha = input("Digite uma opção: ").strip()
    return escolha

# catalogo dos professores
def catalogo_professor():
    print(f'=' * 75)
    print(f'|{" Painel do Professor ":=^73}|')
    print(f'=' * 75)
    print(f'|{" 1 - Lançar/Atualizar Nota":<73}|')
    print(f'|{" 2 - Listar Notas por Aluno":<73}|')
    print(f'|{" 3 - Listar Notas de Todos os Alunos da matéria":<73}|')
    print(f'|{" 0 - Logout":<73}|')
    print(f'=' * 75)

    escolha = input("Digite uma opção: ").strip()
    return escolha

# catalogo dos alunos
def catalogo_aluno():
    print(f'=' * 75)
    print(f'|{" Painel do Aluno ":=^73}|')
    print(f'=' * 75)
    print(f'|{" 1 - Ver Minhas Notas":<73}|')
    print(f'|{" 0 - Logout":<73}|')
    print(f'=' * 75)

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
                    elif e == "3":
                        listar_notas_do_professor()
                    else:
                        print("Opção inválida. Tente novamente.")

            elif tipo == 'aluno':
                print("\nCarregando suas notas...")
                id_aluno = id_aluno_por_usuario(user["id_usuario"])
                if id_aluno:
                    listar_notas_por_aluno(id_aluno=id_aluno)
                else:
                    print("Seu usuário não está vinculado a um aluno no sistema.")

            else:
                print("Tipo de usuário não reconhecido.")

        elif escolha == "2":
            criar_usuario()

        else:
            print("Opção inválida. Digite apenas números válidos.")


if __name__ == "__main__":
    main()