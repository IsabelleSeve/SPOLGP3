from enum import Enum

class Usuario:
    def __init__(self, id, nome, email):
        self.id = id
        self.nome = nome
        self.email = email

    def __str__(self):
        return f"ID: {self.id:^3}| Nome: {self.nome:^20}| Email: {self.email:^30}|"

class Projeto:
    def __init__(self, id, nome, descricao):
        self.id = id
        self.nome = nome
        self.descricao = descricao

    def __str__(self):
        return f"ID: {self.id:^3}, Projeto: {self.nome:^20}"

class Categoria:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    def __str__(self):
        return f"ID: {self.id:^3}, Categoria: {self.nome:^10}"

class Status(Enum):
    A_FAZER = "A fazer"
    FAZENDO = "Fazendo"
    FEITO = "Feito"

class Prioridade(Enum):
    BAIXA = "Baixa"
    MEDIA = "Media"
    ALTA = "Alta"

class Tarefa:
    def __init__(self, id, titulo, descricao, projeto, responsavel, categoria, prioridade, status, criacao, prazo ):
        self.id = str(id)
        self.titulo = titulo
        self.descricao = descricao
        self.projeto = projeto
        self.responsavel = responsavel
        self.categoria = categoria
        self.prioridade = prioridade
        self.status = status
        self.criacao = str(criacao)
        self.prazo = str(prazo)
        self.excluida = str(False)

    def __str__(self):
        # evita usar formatação direta com especificador sobre objetos
        categoria_str = getattr(self.categoria, "nome", str(self.categoria))
        projeto_str = getattr(self.projeto, "nome", str(self.projeto))
        responsavel_str = getattr(self.responsavel, "nome", str(self.responsavel))

        return (
            f"{'='*50}\n"
            f"|{'Tarefa ' + self.id:<50}|\n"
            f"|{'Título: ' + self.titulo:<50}|\n"
            f"|{'Descrição: ' + self.descricao:<50}|\n"
            f"|{'Projeto: ' + projeto_str:<50}|\n"
            f"|{'Responsável: ' + responsavel_str:<50}|\n"
            f"|{'Categoria: ' + categoria_str:<50}|\n"
            f"|{'Prioridade: ' + self.prioridade:<50}|\n"
            f"|{'Status: ' + self.status:<50}|\n"
            f"|{'Criada em: ' + self.criacao:<50}|\n"
            f"|{'Prazo: ' + self.prazo:<50}|\n"
            f"|{'Excluída: ' + self.excluida:<50}|\n"
            f"{'=' * 52}\n"
        )


