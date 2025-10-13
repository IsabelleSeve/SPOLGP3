from os.path import join
from classes import Usuario, Projeto, Categoria, Status, Tarefa, Prioridade
from datetime import datetime


usuarios = []
projetos = []
categorias = []
tarefas = []

def inserirValorObrigatio(prompt):
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        else:
            print("Esse campo necessariamente precisa ser preenchido")

# CRIANDO O CRUD PARA O USUÁRIO
# CREATE
def criarUsuario():
    id = len(usuarios) + 1
    nome = inserirValorObrigatio("Digite o nome do usuario: ")
    email = input("Digite o email do usuario: ")

    usuario = Usuario(id, nome, email)
    usuarios.append(usuario)
    print("Usuario criado com sucesso!")
    return usuario

# READ
def mostrarUsuarios():
    if (len(usuarios) == 0):
        print("Não há usuário cadastrado!")
        return

    print(f"{' Exibindo usuários cadastrados ':=^60}")
    for usuario in usuarios:
        print(usuario)

# UPDATE
def editarUsuario():
    mostrarUsuarios()
    try:
        id = int(input("Digite o id do usuario que deseja editar: "))
        if (len(usuarios) == 0):
            print("Não há usuários cadastrados")

        else:
            for usuario in usuarios:
                if usuario.id == id:
                    novoNome = input("Digite o novo nome do usuario : ") or usuario.nome
                    novoEmail = input("Digite o novo email do usuario: ") or usuario.email

                    usuario.nome = novoNome
                    usuario.email = novoEmail

                    print("Usuario atualizado com sucesso!")
                    return
            print("Digite um id de usuário presente na lista!")
    except ValueError:
        print("Digite uma informação válida!")


# CRIANDO O CRUD PARA O CATEGORIA
# CREATE
def criarCategoria():
    id = len(categorias) + 1
    nome = inserirValorObrigatio("Digite o nome do categoria: ")

    categoria = Categoria(id, nome)
    categorias.append(categoria)
    print("Categoria criada com sucesso!")
    return categoria

# READ
def mostrarCategoria():
    if (len(categorias) == 0):
        print("Nenhuma cadastrada!")
        return
    print(f"{'Exibindo categorias':=^20}")
    for categoria in categorias:
        print(categoria)

# UPDATE
def editarCategoria():
    mostrarCategoria()
    try:
        id = int(input("Digite o id do categoria que deseja editar: "))
        for categoria in categorias:
            if categoria.id == id:
                novoNome = inserirValorObrigatio(f"Nome novo: ") or categoria.nome

                categoria.nome = novoNome

                print("Categoria atualizada com sucesso!")
                return
        print("Digite um id de categoria presente na lista!")
    except ValueError:
        print("Digite uma informação válida!")


# CRIANDO CRUD PARA PROJETO -- SIMPLIFICADO
# CREATE
def criarProjeto():
    id = len(projetos)+1
    nome = inserirValorObrigatio("Digite o nome do projeto: ")
    descricao = input("Digite o descricao do projeto: ")

    projeto = Projeto(id, nome, descricao)
    projetos.append(projeto)
    print("Projeto criado com sucesso!")
    return projeto

# READ
def mostrarProjeto():
    if (len(projetos) == 0):
        print("Nenhuma projeto!")
        return
    print(f"{' Exibindo projetos ':=^50}")
    for projeto in projetos:
        print(projeto)

# UPDATE
def editarProjeto():
    mostrarProjeto()
    try:
        id = int(input("Digite o id do projeto: "))
        for projeto in projetos:
            if projeto.id == id:
                novoNome = inserirValorObrigatio(f"Novo nome: ") or projeto.nome
                novaDescricao = input(f"Atulização da descrição: ") or projeto.descricao

                projeto.nome = novoNome
                projeto.descricao = novaDescricao

                print("Projeto atualizado com sucesso!")
                return
        print("Digite um id de projeto presente na lista!")
    except ValueError:
        print("Digite uma informação válida!")

# CRIANDO CRUD PARA TAREFA -- SIMPLIFICADO
# CREATE
def criarTarefa():
    id = len(tarefas)+1
    titulo = str(inserirValorObrigatio("Digite o título do tarefa: "))
    descricao = str(input("Digite o descricao do tarefa: "))
    while True:
        try:
            criacao = datetime.strptime(input("Digite data e hora de criação da tarefa (dd/mm/aaaa hh:mm) : "), "%d/%m/%Y %H:%M")
            prazo = datetime.strptime(inserirValorObrigatio("Digite o prazo do tarefa (dd/mm/aaaa hh:mm): "), "%d/%m/%Y %H:%M")
            break
        except ValueError:
            print("Digite as informações exatamente como solicitadas!")

    # Escolhendo quem ficará responsável pela tarefa
    print(f'{"Associando Tarefa a um Responsável":=^50}')
    print(f"|{'Usuários':^50}|")
    print(mostrarUsuarios())

    #Caso nao tenha usuarios cadastrados
    if not usuarios:
        print("Crie um novo!")
        responsavel = criarUsuario()
    else:
        responsavelId = int(input("Digite o ID do Responsável da tarefa: "))
        responsavel = next((u for u in usuarios if u.id == responsavelId), None)

        if not responsavel:
            print("Digite apenas o ID de um usuário existente!")
            reponsavel = criarUsuario()


    #Escolhendo a categoria para a tarefa
    print(f'{"Associando Tarefa a uma Categoria":=^50}')
    print(f"|{'Categorias':<40}|")
    print(mostrarCategoria())

    #Caso nao tenha Categorias cadastradas
    if not categorias:
        print("Não existe nenhuma categoria cadastrada, crie uma nova!")
        categoria = criarCategoria()
    else:
        categoria_id = int(input("Digite o ID da categoria: "))
        categoria = next((c for c in categorias if c.id == categoria_id), None)

        if not categoria:
            print("Categoria não encontrada! Crie uma nova categoria!.")
            categoria = criarCategoria()

    # Escolhendo o projeto que ele vai fazer parte
    print(f"\n{'Associando Tarefa a uma Projeto':=^50}")
    print(f"|{'Projetos':<40}|")
    print(mostrarProjeto())

    #Caso nao tenha Projetos cadastrados
    if not projetos:
        print("Nenhuma projeto cadastrado, crie um novo!")
        projeto = criarProjeto()
    else:
        projeto_id = int(input("Digite o ID da categoria: "))
        projeto = next((c for c in projetos if c.id == projeto_id), None)

        if not projeto:
            print("Projeto não encontrado! Crie um novo.")
            projeto = criarProjeto()

    #Definindo Prioridade e Status
    prioridade = input("Digite a prioridade da tarefa (baixa/média/alta): ").capitalize()
    status = input("Digite o status inicial da tarefa (ex: Pendente, Em andamento, Concluída): ").capitalize()

    # Criar o objeto tarefa
    nova_tarefa = Tarefa(id, titulo, descricao, projeto, responsavel, categoria, prioridade, status, criacao, prazo)
    tarefas.append(nova_tarefa)
    print("\nTarefa criada com sucesso!")
    print(nova_tarefa)

# READ
def mostrarTarefa():
    if (len(tarefas) == 0):
        print("Nenhuma tarefa cadastrada ainda!")
        return
    print(f"{' Exibindo Tarefas ':=^50}")
    for tarefa in tarefas:
        print(tarefa)

# UPDATE
def editarTarefa():
    # Caso nao tenha tarefas cadastradas
    if not tarefas:
        print("Nenhuma tarefa cadastrada ainda! Crie uma nova:")
        criarTarefa()
        return

    mostrarTarefa()
    try:
        id = int(input("Digite o ID do Tarefa: "))
    except ValueError:
        print("Digite uma informação válida!")
        return

    encontrarTarefa = next((t for t in tarefas if t.id == id), None)

    if not encontrarTarefa:
        print("Digite uma informação válida!")
        return

    t = encontrarTarefa
    # Editando o Titulo e a Descricao
    t.titulo = str(input("Digite o titulo do Tarefa: ")) or t.titulo
    t.descricao = str(input("Digite o descricao do Tarefa: ")) or t.descricao
    # Editando o prazo criando um validador para a o datetime
    while True:
        novoPrazo = input("Digite o novo prazo (dd/mm/aaaa hh:mm): ")
        if not novoPrazo:
            break
        try:
            t.prazo = datetime.strptime(novoPrazo, "%d/%m/%Y %H:%M")
            break
        except ValueError:
            print("Digite as informações exatamente como solicitadas!")
    # Editando a categoria com categorias já cadastradas
    mostrarCategoria()
    novaCategoriaId = int(input("Digite o ID da categoria pelo qual deseja trocar"))
    if novaCategoriaId:
        try:
            novaCategoria_Id = int(novaCategoriaId)
            novaCategoria = next((c for c in categorias is c.id == novaCategoriaId), None)

            if novaCategoria:
                t.categoria = novaCategoria
                print("Categoria alterada com sucesso!")
            else:
                print("Digite um ID de Categoria Válido!")
        except ValueError:
            print("ID invalida!")

    # Alterando a prioridade
    listaPropriedades = [p.value.lowe() for p in Prioridade]
    print(f"{'Exibindo Prioridade':=^25}")
    print(f"Opções: {', ',join(Prioridade._member_names_)}")

    novaPrioridade = input("Digite o Prioridade do Tarefa: ").upper()
    if novaPrioridade:
        try:
            novaPrioridadeEnum = Prioridade[novaPrioridade]
            t.prioridade = novaPrioridadeEnum.value
            print("Prioridade alterada com sucesso!")
        except ValueError:
            print("Prioridade Inválida. Será mantida a original")

    # Alterando Status
    listaStatus = [s.value.lower() for s in Status]
    print(f"{'Exibindo Status':=^25}")
    print(f"Opções: {', '.join(Status._member_names_)}")

    novoStatus = input(f"Digite o Status do Tarefa: {t.status}").upper()

    if novoStatus:
        try:
            novoStatusEnum = Status[novoStatus]
            t.status = novoStatusEnum.value
            print("Status alterada com sucesso!")
        except ValueError:
            print(f"Ststus inválido.")

    #Alterando Projeto
    print(f"{'Exibindo Projeto':=^25}")
    mostrarProjeto()

    novoProjetoId = int(input("Digite o ID do Projeto para a Tarefa: ")).upper()

    if novoProjetoId:
        try:
            novoProjetoId_ = int(novoProjetoId)
            novoProjeto = next((p for p in projetos if p.id == novoProjetoId_), None)

            if novoProjeto:
                t.projeto = novoProjeto
                print("Projeto alterada com sucesso!")
            else:
                print("ID inválido! Projeto não alterado")
        except ValueError:
            print("ID inválido! Projeto não alterado")
    print("\n" + "=" * 60)
    print("✨ Tarefa atualizada com sucesso!")

# DELETANDO ENTIDADES (CRIAR VALIDADORES)
# DELETE USUÁRIO
def apagarUsuario():
    mostrarUsuarios()
    try:
        id = int(input("Digite o id do usuario que deseja apagar: "))
        for usuario in usuarios:
            if usuario.id == id:
                usuario.remove(usuario)
                print("Usuario apagado com sucesso!")
                return
            print("Digite um id de usuario presente na lista!")
    except ValueError:
        print("Digite um número válido!")

# DELETE CATEGORIA
def apagarCategoria():
    mostrarCategoria()
    try:
        print("Não apagar categorias que estejam associadas a Tarefas e Projetos!")
        id = int(input("Digite o id da categoria que deseja apagar:"))
        for categoria in categorias:
            if categoria.id == id:
                categoria.remove(categorias)
                print("Categoria apagada com sucesso!")
                return
        print("Digite um id de categoria presente na lista!")
    except ValueError:
        print("Digite uma informação válida")

# DELETE PROJETO
def apagarProjeto():
    mostrarProjeto()
    try:
        id = int(input("Digite o id do projeto: "))
        for projeto in projetos:
            if projeto.id == id:
                projetos.remove(projeto)
                print("Projeto apagado com sucesso!")
                return
        print("Digite um id de projeto presente na lista!")
    except ValueError:
        print("Digite uma informação válida!")

# Criando Catálogo de opções
def catalogo():
    while True:
        print(f'-'*40)
        print(f'|{"Catálogo":^38}|')
        print(f'-'*40)
        print(f'|{" 1 - Gerenciamento de Usuários":<38}|')
        print(f'|{" 2 - Gerenciamento de Categorias":<38}|')
        print(f'|{" 3 - Gerenciamento de Projetos":<38}|')
        print(f'|{" 4 - Gerenciamento de Tarefas":<38}|')
        print(f'|{" 0 - Sair":<38}|')
        print(f'-'*40)

        try:
            resposta = int(input("Digite uma opção: "))
        except ValueError:
            print("Por favor, digite apenas números.")
            continue


        # Criando as respostas para o Catálogo
        # CRUD DO USUARIO
        if resposta == 1:
            print(f'=' * 40)
            print(f'|{" Gerenciamento de Usuários ":=^38}|')
            print(f'=' * 40)
            print(f'|{" 1 - Criar Usuário":<38}|')
            print(f'|{" 2 - Lista de Usuários cadastrados":<38}|')
            print(f'|{" 3 - Editar Usuário cadastrados":<38}|')
            print(f'|{" 4 - Deletar Usuário cadastrado":<38}|')
            print(f'=' * 40)

            try:
                resp1 = int(input("Digite uma opção: "))
            except ValueError:
                print("Por favor, digite apenas números.")
                continue

            if resp1 == 1:
                criarUsuario()
            elif resp1 == 2:
                mostrarUsuarios()
            elif resp1 == 3:
                editarUsuario()
            elif resp1 == 4:
                apagarUsuario()

        #CRUD DA CATEGORIA
        elif resposta == 2:
            print(f'=' * 40)
            print(f'|{" Gerenciamento de Categorias ":=^38}|')
            print(f'=' * 40)
            print(f'|{" 1 - Criar Categoria":<38}|')
            print(f'|{" 2 - Lista de Categorias cadastradas":<38}|')
            print(f'|{" 3 - Editar Categorias cadastradas":<38}|')
            print(f'|{" 4 - Deletar Categoria cadastrada":<38}|')
            print(f'=' * 40)

            try:
                resp2 = int(input("Digite uma opção: "))
            except ValueError:
                print("Por favor, digite apenas números.")
                continue

            if resp2 == 1:
                criarCategoria()
            elif resp2 == 2:
                mostrarCategoria()
            elif resp2 == 3:
                editarCategoria()
            elif resp2 == 4:
                apagarCategoria()

        #CRUD DO PROJETO
        elif resposta == 3:
            print(f'=' * 40)
            print(f'|{" Gerenciamento de Projetos ":=^38}|')
            print(f'=' * 40)
            print(f'|{" 1 - Criar Projeto":<38}|')
            print(f'|{" 2 - Lista de Projetos cadastrados":<38}|')
            print(f'|{" 3 - Editar Projetos cadastrados":<38}|')
            print(f'|{" 4 - Deletar Projeto cadastrado":<38}|')
            print(f'=' * 40)

            try:
                resp3 = int(input("Digite uma opção: "))
            except ValueError:
                print("Por favor, digite apenas números.")
                continue

            if resp3 == 1:
                criarProjeto()
            elif resp3 == 2:
                mostrarProjeto()
            elif resp3 == 3:
                editarProjeto()
            elif resp3 == 4:
                apagarProjeto()

        # CRUD DO TAREFAS
        elif resposta == 4:
            print(f'=' * 40)
            print(f'|{" Gerenciamento de Tarefas ":=^38}|')
            print(f'=' * 40)
            print(f'|{" 1 - Criar Tarefa":<38}|')
            print(f'|{" 2 - Lista de Tarefas cadastrados":<38}|')
            print(f'|{" 3 - Editar Tarefas cadastrados":<38}|')
            print(f'|{" 4 - Deletar Tarefa cadastrado":<38}|')
            print(f'=' * 40)

            try:
                resp4 = int(input("Digite uma opção: "))
            except ValueError:
                print("Por favor, digite apenas números.")
                continue

            if resp4 == 1:
                criarTarefa()

            elif resp4 == 2:
                mostrarTarefa()

            elif resp4 == 3:
                editarTarefa()

            elif resp4 == 4:
                apagarTarefa()

        elif resposta == 0:
            print("encerando...")
            break
        else:
            print("Esta opção não existe, por gentileza escolha outra.")
            continue


if __name__ == "__main__":
    catalogo()

