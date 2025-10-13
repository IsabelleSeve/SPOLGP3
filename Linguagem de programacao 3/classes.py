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
    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDA = "Concluída"

class Prioridade(Enum):
    BAIXA = "Baixa"
    MEDIA = "Media"
    ALTA = "Alta"

class Tarefa:
    def __init__(self, id, titulo, descricao, projeto, responsavel, categoria, prioridade, status, criacao, prazo ):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.projeto = projeto
        self.responsavel = responsavel
        self.categoria = categoria
        self.prioridade = prioridade
        self.status = status
        self.criacao = criacao
        self.prazo = prazo

    def __str__(self):
        return f"""
            Tarefa ID {self.id:^3}: Título: {self.titulo:^10} | Projeto: {self.projeto.nome:^17} |\n
            Responsável: {self.responsavel.nome} | Status: {self.status:^15} | Categoria: {self.categoria:^10}| \m
            Prioridade: {self.prioridade:^15} | Prazo: {self.prazo:^15}
        """


