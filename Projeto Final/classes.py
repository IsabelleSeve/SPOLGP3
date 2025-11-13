from enum import Enum

class Usuario:
    def __init__(self, id_usuario, nome, email, cpf=None, senha=None, tipo_usuario=None, ativo=True):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.senha = senha
        self.tipo_usuario = tipo_usuario
        self.ativo = ativo

    def __str__(self):
        return f"[{self.tipo_usuario.upper():^12}] ID: {self.id_usuario:^3} | Nome: {self.nome:^20} | Email: {self.email:^30}"


class Turma:
    def __init__(self, id_turma, nome_turma, ano_letivo, turno):
        self.id_turma = id_turma
        self.nome_turma = nome_turma
        self.ano_letivo = ano_letivo
        self.turno = turno

    def __str__(self):
        return f"Turma {self.nome_turma} ({self.turno}) - Ano: {self.ano_letivo}"


class Materia:
    def __init__(self, id_materia, nome_materia, carga_horaria=None, descricao=None):
        self.id_materia = id_materia
        self.nome_materia = nome_materia
        self.carga_horaria = carga_horaria
        self.descricao = descricao

    def __str__(self):
        return f"[{self.id_materia:^3}] {self.nome_materia} ({self.carga_horaria}h)"


class Aluno:
    def __init__(self, id_aluno, id_usuario, matricula_aluno, data_nascimento=None, id_turma=None):
        self.id_aluno = id_aluno
        self.id_usuario = id_usuario
        self.matricula_aluno = matricula_aluno
        self.data_nascimento = data_nascimento
        self.id_turma = id_turma

    def __str__(self):
        return f"Aluno {self.matricula_aluno} (Usuário {self.id_usuario}) - Turma: {self.id_turma}"


class Professor:
    def __init__(self, id_professor, id_usuario, matricula_professor, formacao=None):
        self.id_professor = id_professor
        self.id_usuario = id_usuario
        self.matricula_professor = matricula_professor
        self.formacao = formacao

    def __str__(self):
        return f"Professor {self.matricula_professor} - Formação: {self.formacao}"


class Nota:
    def __init__(self, id_nota, id_aluno, id_materia, id_professor,
                 nota1=None, nota2=None, nota3=None, recuperacao=None, nota_final=None, ano_letivo=None):
        self.id_nota = id_nota
        self.id_aluno = id_aluno
        self.id_materia = id_materia
        self.id_professor = id_professor
        self.nota1 = nota1
        self.nota2 = nota2
        self.nota3 = nota3
        self.recuperacao = recuperacao
        self.nota_final = nota_final
        self.ano_letivo = ano_letivo

    def calcular_media(self):
        notas = [n for n in [self.nota1, self.nota2, self.nota3] if n is not None]
        if notas:
            media = sum(notas) / len(notas)
            if self.recuperacao is not None:
                media = max(media, self.recuperacao)
            self.nota_final = round(media, 2)
        return self.nota_final

    def __str__(self):
        return (f"Aluno {self.id_aluno} | Matéria {self.id_materia} | "
                f"Notas: [{self.nota1}, {self.nota2}, {self.nota3}] | Final: {self.nota_final}")


class ProfessorMateria:
    def __init__(self, id_professor, id_materia):
        self.id_professor = id_professor
        self.id_materia = id_materia

    def __str__(self):
        return f"Prof {self.id_professor} ↔ Matéria {self.id_materia}"


class TurmaMateria:
    def __init__(self, id_turma, id_materia):
        self.id_turma = id_turma
        self.id_materia = id_materia

    def __str__(self):
        return f"Turma {self.id_turma} ↔ Matéria {self.id_materia}"
