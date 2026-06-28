# ============================================================
# MERCADO PYTHON
# ============================================================
# Sistema de mercado desenvolvido em Python para trabalho do curso.
#
# Autores:
# - Davi Delmondes (@davi-delmondes)
# - João Marcelo (@Joaomarcelloo-dev)
# - João Daniel (@joao-daniell)
# - Lorrã Myguel (@lorra-myguel)
#
# Repositório original:
# https://github.com/davi-delmondes/mercado-python
#
# Curso: Desenvolvimento de Sistemas
# Ano: 2026
# ============================================================


import os
from datetime import datetime
import math
import json
from typing import Callable, Optional


# ============================================================
# DADOS GLOBAIS DO SISTEMA
# ============================================================
# Estrutura de usuarios:  {nome: [senha, tipo]}
# Estrutura de produtos:  {nome: (preco, estoque)}
# Estrutura de carrinhos: {cliente: [[produto, qtd, total], ...]}
# Estrutura de vendas:    [{"cliente": ..., "data": ..., "itens": [...]}, ...]

usuarios: dict = {}
produtos: dict = {}
carrinhos_usuarios: dict = {}
vendas: list = []

ARQUIVO_DADOS = "dados_mercado_python.json"


# ============================================================
# PERSISTÊNCIA DE DADOS COM JSON
# ============================================================

def carregar_dados() -> dict:
    """Carrega os dados do arquivo JSON.

    Realiza migração automática caso o arquivo ainda use o formato antigo
    com três listas paralelas (vendas, data_vendas, clientes_vendas).
    """
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        # Migração: formato antigo → novo (lista de dicionários).
        if "data_vendas" in dados and "clientes_vendas" in dados:
            dados["vendas"] = [
                {"cliente": cliente, "data": data, "itens": itens}
                for cliente, data, itens in zip(
                    dados.get("clientes_vendas", []),
                    dados.get("data_vendas", []),
                    dados.get("vendas", []),
                )
            ]

        return dados

    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "usuarios": {},
            "produtos": {},
            "carrinhos_usuarios": {},
            "vendas": [],
        }


def salvar_dados() -> None:
    """Salva todos os dados do sistema no arquivo JSON."""
    dados = {
        "usuarios": usuarios,
        "produtos": produtos,
        "carrinhos_usuarios": carrinhos_usuarios,
        "vendas": vendas,
    }
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


# Carrega os dados ao iniciar o programa.
_dados_salvos = carregar_dados()
usuarios = _dados_salvos["usuarios"]
produtos = _dados_salvos["produtos"]
carrinhos_usuarios = _dados_salvos["carrinhos_usuarios"]
vendas = _dados_salvos["vendas"]


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pausa() -> None:
    print()
    input("Pressione ENTER para continuar...")


def ler_numero(tipo: str, mensagem: str, tela: Optional[Callable] = None) -> int | float:
    """Lê e valida um número inteiro ("int") ou decimal ("float") do usuário.

    Em caso de entrada inválida, exibe erro e chama `tela()` para redesenhar
    a tela atual, ou limpa o terminal se nenhuma tela for fornecida.
    """
    while True:
        try:
            entrada = input(mensagem)
            if tipo == "int":
                resultado = int(entrada)
            else:
                resultado = float(entrada.replace(",", "."))
                if not math.isfinite(resultado):
                    raise ValueError
            print()
            return resultado
        except ValueError:
            print()
            print("❌ Erro: digite um número válido!")
            pausa()
            if tela is not None:
                tela()
            else:
                limpar_tela()


def erro() -> bool:
    """Pergunta ao usuário se deseja tentar novamente ou voltar ao menu.

    Retorna True para tentar novamente, False para voltar ao menu.
    """
    while True:
        print()
        print("[1] Tentar novamente")
        print("[0] Voltar ao menu")
        print()
        opcao = ler_numero("int", "Escolha uma opção: ")
        if opcao == 1:
            limpar_tela()
            return True
        if opcao == 0:
            limpar_tela()
            return False
        print("❌ Opção inválida! Digite apenas 0 ou 1.")
        pausa()


# ============================================================
# FUNÇÕES DE CÁLCULO
# ============================================================

def calcular_estoque_disponivel(nome_produto: str, usuario_logado: str) -> int:
    """Retorna o estoque disponível descontando o que já está no carrinho do cliente."""
    carrinho = carrinhos_usuarios[usuario_logado]
    estoque_total = produtos[nome_produto][1]
    ja_reservado = sum(item[1] for item in carrinho if item[0] == nome_produto)
    return estoque_total - ja_reservado


# ============================================================
# TELAS — MENUS PRINCIPAIS
# ============================================================

def mostrar_menu_inicial() -> None:
    limpar_tela()
    print("=" * 40)
    print("🛒 MERCADO PYTHON 🛒".center(40))
    print("=" * 40)
    print()
    print("[1] 🔐 Fazer Login")
    print("[2] 📝 Cadastrar Usuário")
    print("[0] 🚪 Sair")
    print()


def mostrar_menu_admin() -> None:
    limpar_tela()
    print("🛠️  PAINEL DO ADMINISTRADOR 🛠️")
    print()
    print("[1] 📦 Cadastrar Produto")
    print("[2] 📋 Listar Produtos")
    print("[3] ✏️  Editar Produto")
    print("[4] 📊 Relatório de Vendas")
    print("[5] 🔄 Limpar Dados do Mercado")
    print("[0] 🚪 Sair")
    print()


def mostrar_menu_cliente() -> None:
    limpar_tela()
    print("🛒 PAINEL DO CLIENTE 🛒")
    print()
    print("[1] 📋 Listar Produtos")
    print("[2] 🛒 Comprar Produto")
    print("[3] 🧺 Ver Carrinho")
    print("[4] 🗑️  Remover Item do Carrinho")
    print("[5] 💳 Finalizar Compra")
    print("[0] 🚪 Sair")
    print()


# ============================================================
# TELAS — USUÁRIOS
# ============================================================

def mostrar_tela_tipo_usuario(cadastro_usuario: str) -> None:
    limpar_tela()
    print("📝 CADASTRO 📝".center(40))
    print()
    print(f"👤 Usuário: {cadastro_usuario}")
    print("🔒 Senha: cadastrada e confirmada")
    print()
    print("Tipo de usuário:")
    print()
    print("[1] Administrador")
    print("[2] Cliente")
    print()
    print("[0] Cancelar cadastro")
    print()


# ============================================================
# TELAS — PRODUTOS E EDIÇÃO
# ============================================================

def mostrar_titulo_produto() -> None:
    limpar_tela()
    print("📦 CADASTRAR PRODUTO")
    print()


def mostrar_tela_preco_produto(nome_produto: str) -> None:
    mostrar_titulo_produto()
    print(f"Nome do produto: {nome_produto}")
    print()


def mostrar_tela_quantidade_produto(nome_produto: str, preco_produto: float) -> None:
    mostrar_titulo_produto()
    print(f"Nome do produto: {nome_produto}")
    print()
    print(f"Preço do produto: R$ {preco_produto:.2f}")
    print()


def mostrar_tela_editar_produtos() -> None:
    limpar_tela()
    print("✏️  EDITAR PRODUTO")
    print()
    print("Produtos cadastrados:")
    print()
    for i, (nome, (preco, estoque)) in enumerate(produtos.items(), start=1):
        print(f"{i} - {nome} | R$ {preco:.2f} | Estoque: {estoque}")
    print()
    print("[0] Cancelar")
    print()


def mostrar_tela_opcoes_editar_produto(nome_produto: str) -> None:
    limpar_tela()
    print("✏️  EDITAR PRODUTO")
    print()
    print(f"📦 Produto escolhido: {nome_produto}")
    print(f"💰 Preço atual: R$ {produtos[nome_produto][0]:.2f}")
    print(f"📦 Estoque atual: {produtos[nome_produto][1]}")
    print()
    print("O que deseja editar?")
    print()
    print("[1] Alterar preço")
    print("[2] Alterar estoque total")
    print("[3] Acrescentar quantidade ao estoque")
    print("[0] Cancelar")
    print()


def mostrar_tela_alterar_estoque(titulo: str, nome_produto: str) -> None:
    limpar_tela()
    print(titulo)
    print()
    print(f"📦 Produto: {nome_produto}")
    print(f"📦 Estoque atual: {produtos[nome_produto][1]}")
    print()


def mostrar_tela_alterar_preco(nome_produto: str) -> None:
    limpar_tela()
    print("✏️  ALTERAR PREÇO")
    print()
    print(f"📦 Produto: {nome_produto}")
    print(f"💰 Preço atual: R$ {produtos[nome_produto][0]:.2f}")
    print()


# ============================================================
# TELAS — COMPRA, CARRINHO E FINALIZAÇÃO
# ============================================================

def mostrar_titulo_comprar(usuario_logado: str) -> None:
    limpar_tela()
    print("🛒 COMPRAR PRODUTO")
    print()
    for i, (nome, (preco, _)) in enumerate(produtos.items(), start=1):
        estoque = max(0, calcular_estoque_disponivel(nome, usuario_logado))
        print(f"{i} - {nome} | R$ {preco:.2f} | Estoque: {estoque}")
    print()
    print("[0] Voltar ao menu")
    print()


def mostrar_produto_escolhido(posicao_produto: int, estoque_disponivel: int) -> None:
    limpar_tela()
    print("🛒 COMPRAR PRODUTO")
    print()
    for i, (nome, (preco, _)) in enumerate(produtos.items()):
        if i == posicao_produto:
            print(f"📦 Produto escolhido: {nome}")
            print(f"💰 Preço unitário: R$ {preco:.2f}")
            print(f"📦 Estoque disponível: {estoque_disponivel}")
            print()
            break


def mostrar_menu_comprar_outro() -> None:
    print("Deseja comprar outro produto?")
    print()
    print("[1] Sim")
    print("[0] Voltar ao menu")
    print()


def mostrar_tela_remover_item_carrinho(usuario_logado: str) -> None:
    carrinho = carrinhos_usuarios[usuario_logado]
    limpar_tela()
    print("🗑️  REMOVER ITEM DO CARRINHO")
    print()
    print("Itens no carrinho:")
    print()
    for i, item in enumerate(carrinho, start=1):
        print(f"{i} - {item[0]} | Quantidade: {item[1]} | Total: R$ {item[2]:.2f}")
    total = sum(item[2] for item in carrinho)
    print()
    print(f"💰 Total do carrinho: R$ {total:.2f}")
    print()
    print("[0] Cancelar")
    print()


def mostrar_menu_remover_outro_item() -> None:
    print()
    print("Deseja remover outro item?")
    print()
    print("[1] Sim")
    print("[0] Voltar ao menu")
    print()


def mostrar_titulo_finalizar_compra(total_carrinho: float, usuario_logado: str) -> None:
    carrinho = carrinhos_usuarios[usuario_logado]
    limpar_tela()
    print("💳 FINALIZAR COMPRA")
    print()
    print("📦 Itens comprados:")
    print()
    for i, item in enumerate(carrinho, start=1):
        print(f"{i} - {item[0]} | Quantidade: {item[1]} | Total: R$ {item[2]:.2f}")
    print()
    print("━" * 40)
    print()
    print(f"💰 Total da compra: R$ {total_carrinho:.2f}")
    print()


def mostrar_menu_confirmar_compra() -> None:
    print("Deseja confirmar a compra?")
    print()
    print("[1] Confirmar compra")
    print("[0] Cancelar")
    print()


def mostrar_tela_confirmar_compra(total_carrinho: float, usuario_logado: str) -> None:
    mostrar_titulo_finalizar_compra(total_carrinho, usuario_logado)
    mostrar_menu_confirmar_compra()


def mostrar_tela_limpar_dados() -> None:
    limpar_tela()
    print("🔄 LIMPAR DADOS DO MERCADO")
    print()
    print("⚠️ Atenção!")
    print("Essa opção irá apagar todos os dados do mercado:")
    print()
    print("- Produtos cadastrados")
    print("- Preços")
    print("- Estoques")
    print("- Carrinhos dos clientes")
    print("- Vendas realizadas")
    print("- Datas das vendas")
    print()
    print("Os usuários cadastrados serão mantidos.")
    print()
    print("Deseja realmente limpar os dados do mercado?")
    print()
    print("[1] Sim, limpar dados")
    print("[0] Cancelar")
    print()


# ============================================================
# USUÁRIOS E LOGIN
# ============================================================

def cadastrar_usuario() -> None:
    limpar_tela()

    while True:
        print("📝 CADASTRO 📝".center(40))
        print()

        cadastro_usuario = input("👤 Digite um usuário: ").strip().title()
        print()

        if not cadastro_usuario:
            print("❌ Usuário não pode ficar vazio!")
            if not erro():
                break
            continue

        if cadastro_usuario in usuarios:
            print("❌ Usuário já cadastrado! Tente outro nome.")
            if not erro():
                break
            continue

        cadastro_senha = input("🔒 Digite uma senha: ").strip()
        print()

        if not cadastro_senha:
            print("❌ Senha não pode ficar vazia!")
            if not erro():
                break
            continue

        confirmacao_senha = input("Confirme sua senha: ").strip()
        print()

        if cadastro_senha != confirmacao_senha:
            print("❌ As senhas não coincidem!")
            if not erro():
                break
            continue

        # Escolha do tipo de usuário.
        while True:
            mostrar_tela_tipo_usuario(cadastro_usuario)

            tipo_usuario = ler_numero(
                "int",
                "Escolha uma opção: ",
                lambda: mostrar_tela_tipo_usuario(cadastro_usuario),
            )

            if tipo_usuario == 0:
                print("❌ Cadastro cancelado!")
                print("Nenhum usuário foi salvo.")
                pausa()
                return

            if tipo_usuario == 1:
                usuarios[cadastro_usuario] = [cadastro_senha, "admin"]
                salvar_dados()
                print("✅ Administrador cadastrado com sucesso!")
                print("👉 Agora você já pode fazer login.")
                pausa()
                limpar_tela()
                break

            elif tipo_usuario == 2:
                usuarios[cadastro_usuario] = [cadastro_senha, "cliente"]
                carrinhos_usuarios[cadastro_usuario] = []
                salvar_dados()
                print("✅ Cliente cadastrado com sucesso!")
                print("👉 Agora você já pode fazer login.")
                pausa()
                limpar_tela()
                break

            else:
                print("❌ Opção inválida! Escolha 1 para Administrador, 2 para Cliente ou 0 para cancelar.")
                pausa()

        break


def fazer_login() -> None:
    limpar_tela()

    while True:
        print("🔐 LOGIN 🔐".center(40))
        print()

        login_usuario = input("👤 Usuário: ").strip().title()

        if login_usuario not in usuarios:
            print()
            print("❌ Usuário não cadastrado!")
            if not erro():
                break
            continue

        login_senha = input("🔒 Senha: ").strip()
        senha_correta = usuarios[login_usuario][0]
        tipo_usuario = usuarios[login_usuario][1]

        if login_senha != senha_correta:
            print()
            print("❌ Senha incorreta!")
            if not erro():
                break
            continue

        print()
        print("✅ Login realizado com sucesso!")
        print()

        if tipo_usuario == "admin":
            print("🚀 Entrando no painel do administrador...")
            pausa()
            limpar_tela()
            menu_admin()
        elif tipo_usuario == "cliente":
            print("🚀 Entrando no painel do cliente...")
            pausa()
            limpar_tela()
            menu_cliente(login_usuario)

        break


# ============================================================
# PRODUTOS E EDIÇÃO DE PRODUTOS
# ============================================================

def cadastrar_produto() -> None:
    limpar_tela()
    print("📦 CADASTRAR PRODUTO")
    print()

    # Cadastro do nome.
    while True:
        nome_produto = input("Nome do produto: ").strip().title()
        print()

        if not nome_produto:
            print("❌ O nome do produto não pode ficar vazio!")
            pausa()
            mostrar_titulo_produto()
            continue

        if nome_produto in produtos:
            print("❌ Produto já cadastrado! Digite outro nome.")
            pausa()
            mostrar_titulo_produto()
            continue

        break

    # Cadastro do preço.
    while True:
        preco_produto = ler_numero(
            "float",
            "Preço do produto: R$ ",
            lambda: mostrar_tela_preco_produto(nome_produto),
        )

        if preco_produto <= 0:
            print("❌ O preço deve ser maior que zero!")
            pausa()
            mostrar_tela_preco_produto(nome_produto)
            continue

        break

    # Cadastro da quantidade em estoque.
    while True:
        quantidade_produto = ler_numero(
            "int",
            "Quantidade em estoque: ",
            lambda: mostrar_tela_quantidade_produto(nome_produto, preco_produto),
        )

        if quantidade_produto <= 0:
            print("❌ A quantidade deve ser maior que zero!")
            pausa()
            mostrar_tela_quantidade_produto(nome_produto, preco_produto)
            continue

        break

    produtos[nome_produto] = (preco_produto, quantidade_produto)
    salvar_dados()

    print("✅ Produto cadastrado com sucesso!")
    pausa()


def listar_produtos() -> None:
    limpar_tela()
    print("📋 LISTA DE PRODUTOS")
    print()

    if not produtos:
        print("❌ Nenhum produto cadastrado!")
        pausa()
        return

    for i, (nome, (preco, estoque)) in enumerate(produtos.items(), start=1):
        print(f"{i} - {nome} | R$ {preco:.2f} | Estoque: {estoque}")

    pausa()


def listar_produtos_cliente(usuario_logado: str) -> None:
    limpar_tela()
    print("📋 PRODUTOS DISPONÍVEIS PARA COMPRA")
    print()

    if not produtos:
        print("❌ Nenhum produto cadastrado!")
        pausa()
        return

    for i, (nome, (preco, _)) in enumerate(produtos.items(), start=1):
        estoque = max(0, calcular_estoque_disponivel(nome, usuario_logado))
        print(f"{i} - {nome} | R$ {preco:.2f} | Estoque: {estoque}")

    pausa()


def editar_produtos() -> None:
    lista_nomes = list(produtos.keys())

    if not lista_nomes:
        limpar_tela()
        print("✏️  EDITAR PRODUTO")
        print()
        print("❌ Nenhum produto cadastrado para editar!")
        pausa()
        return

    while True:
        mostrar_tela_editar_produtos()

        opcao = ler_numero(
            "int",
            "Escolha o número do produto que deseja editar: ",
            mostrar_tela_editar_produtos,
        )

        if opcao == 0:
            print("↩️  Saindo da edição do produto...")
            print()
            print("Retornando ao painel do administrador...")
            pausa()
            return

        if opcao < 1 or opcao > len(lista_nomes):
            print("❌ Produto não encontrado! Escolha uma opção da lista.")
            pausa()
            continue

        nome_produto = lista_nomes[opcao - 1]

        while True:
            mostrar_tela_opcoes_editar_produto(nome_produto)

            opcao_desejada = ler_numero(
                "int",
                "Escolha uma opção: ",
                lambda: mostrar_tela_opcoes_editar_produto(nome_produto),
            )

            if opcao_desejada == 0:
                print("↩️  Saindo da edição do produto...")
                print()
                print("Retornando ao painel do administrador...")
                pausa()
                return

            elif opcao_desejada == 1:
                preco_antigo = produtos[nome_produto][0]

                while True:
                    mostrar_tela_alterar_preco(nome_produto)

                    novo_preco = ler_numero(
                        "float",
                        "Novo preço: R$ ",
                        lambda: mostrar_tela_alterar_preco(nome_produto),
                    )

                    if novo_preco <= 0:
                        print("❌ O preço deve ser maior que zero!")
                        pausa()
                        continue

                    _, estoque_atual = produtos[nome_produto]
                    produtos[nome_produto] = (novo_preco, estoque_atual)

                    # Recalcula os totais dos carrinhos abertos com o novo preço.
                    for carrinho in carrinhos_usuarios.values():
                        for item in carrinho:
                            if item[0] == nome_produto:
                                item[2] = item[1] * novo_preco

                    salvar_dados()

                    print("✅ Preço atualizado com sucesso!")
                    print()
                    print(f"📦 Produto: {nome_produto}")
                    print(f"💰 Preço antigo: R$ {preco_antigo:.2f}")
                    print(f"💰 Novo preço: R$ {novo_preco:.2f}")
                    pausa()
                    break

            elif opcao_desejada == 2:
                estoque_antigo = produtos[nome_produto][1]

                while True:
                    mostrar_tela_alterar_estoque("✏️  ALTERAR ESTOQUE TOTAL", nome_produto)

                    novo_estoque = ler_numero(
                        "int",
                        "Novo estoque total: ",
                        lambda: mostrar_tela_alterar_estoque("✏️  ALTERAR ESTOQUE TOTAL", nome_produto),
                    )

                    if novo_estoque < 0:
                        print("❌ O estoque não pode ser negativo!")
                        pausa()
                        continue

                    preco_atual, _ = produtos[nome_produto]
                    produtos[nome_produto] = (preco_atual, novo_estoque)
                    salvar_dados()

                    print("✅ Estoque atualizado com sucesso!")
                    print()
                    print(f"📦 Produto: {nome_produto}")
                    print(f"📦 Estoque antigo: {estoque_antigo}")
                    print(f"📦 Novo estoque: {novo_estoque}")
                    pausa()
                    break

            elif opcao_desejada == 3:
                estoque_antigo = produtos[nome_produto][1]
                preco_atual = produtos[nome_produto][0]

                while True:
                    mostrar_tela_alterar_estoque("✏️  ACRESCENTAR ESTOQUE", nome_produto)

                    acrescentar = ler_numero(
                        "int",
                        "Quantidade para acrescentar: ",
                        lambda: mostrar_tela_alterar_estoque("✏️  ACRESCENTAR ESTOQUE", nome_produto),
                    )

                    if acrescentar <= 0:
                        print("❌ A quantidade para acrescentar deve ser maior que zero!")
                        pausa()
                        continue

                    novo_estoque = estoque_antigo + acrescentar
                    produtos[nome_produto] = (preco_atual, novo_estoque)
                    salvar_dados()

                    print("✅ Estoque atualizado com sucesso!")
                    print()
                    print(f"📦 Produto: {nome_produto}")
                    print(f"📦 Estoque antigo: {estoque_antigo}")
                    print(f"➕ Quantidade adicionada: {acrescentar}")
                    print(f"📦 Novo estoque: {novo_estoque}")
                    pausa()
                    break

            else:
                print("❌ Opção inválida! Escolha 1, 2, 3 ou 0.")
                pausa()


# ============================================================
# COMPRA E CARRINHO
# ============================================================

def comprar_produtos(usuario_logado: str) -> None:
    carrinho = carrinhos_usuarios[usuario_logado]

    while True:
        limpar_tela()
        print("🛒 COMPRAR PRODUTO")
        print()

        if not produtos:
            print("❌ Nenhum produto cadastrado para compra!")
            pausa()
            break

        for i, (nome, (preco, _)) in enumerate(produtos.items(), start=1):
            estoque = max(0, calcular_estoque_disponivel(nome, usuario_logado))
            print(f"{i} - {nome} | R$ {preco:.2f} | Estoque: {estoque}")

        print()
        print("[0] Voltar ao menu")
        print()

        # Escolha do produto.
        while True:
            escolha = ler_numero(
                "int",
                "Escolha o número do produto: ",
                lambda: mostrar_titulo_comprar(usuario_logado),
            )

            if escolha == 0:
                return

            lista_nomes = list(produtos.keys())

            if escolha < 1 or escolha > len(lista_nomes):
                print("❌ Produto não encontrado! Escolha uma opção da lista.")
                pausa()
                mostrar_titulo_comprar(usuario_logado)
                continue

            nome_escolhido = lista_nomes[escolha - 1]
            preco_produto = produtos[nome_escolhido][0]
            estoque_disponivel = calcular_estoque_disponivel(nome_escolhido, usuario_logado)

            if estoque_disponivel <= 0:
                print("❌ Esse produto está sem estoque no momento!")
                pausa()
                mostrar_titulo_comprar(usuario_logado)
                continue

            break

        mostrar_produto_escolhido(escolha - 1, estoque_disponivel)

        # Escolha da quantidade.
        while True:
            quantidade = ler_numero(
                "int",
                "Quantidade [0 para cancelar item]: ",
                lambda: mostrar_produto_escolhido(escolha - 1, estoque_disponivel),
            )

            if quantidade == 0:
                break

            if quantidade < 0:
                print("❌ A quantidade deve ser maior que zero!")
                pausa()
                mostrar_produto_escolhido(escolha - 1, estoque_disponivel)
                continue

            if quantidade > estoque_disponivel:
                print("❌ Estoque insuficiente!")
                print(f"Estoque disponível: {estoque_disponivel}")
                pausa()
                mostrar_produto_escolhido(escolha - 1, estoque_disponivel)
                continue

            break

        if quantidade == 0:
            continue

        total = preco_produto * quantidade

        # Soma ao item existente no carrinho, ou cria um novo.
        item_existente = next((item for item in carrinho if item[0] == nome_escolhido), None)
        if item_existente:
            item_existente[1] += quantidade
            item_existente[2] += total
        else:
            carrinho.append([nome_escolhido, quantidade, total])

        salvar_dados()

        print("✅ Produto adicionado ao carrinho!")
        print()
        print(f"📦 Produto: {nome_escolhido}")
        print(f"🔢 Quantidade: {quantidade}")
        print(f"💰 Total: R$ {total:.2f}")
        print()

        while True:
            mostrar_menu_comprar_outro()
            opcao = ler_numero("int", "Escolha uma opção: ", mostrar_menu_comprar_outro)
            if opcao in [0, 1]:
                break
            print("❌ Opção inválida! Escolha 1 ou 0.")
            pausa()

        if opcao == 0:
            break


def ver_carrinho(usuario_logado: str) -> None:
    carrinho = carrinhos_usuarios[usuario_logado]

    limpar_tela()
    print("🧺 CARRINHO")
    print()

    if not carrinho:
        print("❌ Carrinho vazio!")
        pausa()
        return

    for i, item in enumerate(carrinho, start=1):
        print(f"{i} - {item[0]} | Quantidade: {item[1]} | Total: R$ {item[2]:.2f}")

    total = sum(item[2] for item in carrinho)
    print()
    print(f"💰 Total do carrinho: R$ {total:.2f}")
    pausa()


def remover_item_carrinho(usuario_logado: str) -> None:
    carrinho = carrinhos_usuarios[usuario_logado]

    limpar_tela()
    print("🗑️  REMOVER ITEM DO CARRINHO")
    print()

    if not carrinho:
        print("❌ Carrinho vazio! Não há itens para remover.")
        pausa()
        return

    while True:
        mostrar_tela_remover_item_carrinho(usuario_logado)

        opcao = ler_numero(
            "int",
            "Escolha o número do item que deseja remover: ",
            lambda: mostrar_tela_remover_item_carrinho(usuario_logado),
        )

        if opcao == 0:
            print("❌ Operação cancelada!")
            print("Nenhum item foi removido.")
            pausa()
            break

        if opcao < 1 or opcao > len(carrinho):
            print("❌ Item não encontrado! Escolha uma opção da lista.")
            pausa()
            continue

        item_removido = carrinho[opcao - 1]
        del carrinho[opcao - 1]
        salvar_dados()

        print("✅ Item removido do carrinho com sucesso!")
        print()
        print(f"📦 Produto removido: {item_removido[0]}")
        print(f"🔢 Quantidade removida: {item_removido[1]}")
        print(f"💰 Total removido: R$ {item_removido[2]:.2f}")

        if not carrinho:
            print()
            print("❌ Carrinho vazio! Não há mais itens para remover.")
            pausa()
            break

        while True:
            mostrar_menu_remover_outro_item()
            remover_outro = ler_numero(
                "int",
                "Escolha uma opção: ",
                mostrar_menu_remover_outro_item,
            )
            if remover_outro == 0:
                print("↩️  Voltando ao menu principal...")
                pausa()
                return
            if remover_outro == 1:
                break
            print("❌ Opção inválida! Escolha 1 ou 0.")
            pausa()


# ============================================================
# FINALIZAÇÃO, RELATÓRIO E LIMPEZA DE DADOS
# ============================================================

def finalizar_compra(usuario_logado: str) -> None:
    carrinho = carrinhos_usuarios[usuario_logado]

    limpar_tela()

    while True:
        print("💳 FINALIZAR COMPRA")
        print()

        if not carrinho:
            print("❌ Carrinho vazio! Adicione produtos antes de finalizar a compra.")
            pausa()
            break

        total_carrinho = sum(item[2] for item in carrinho)

        mostrar_titulo_finalizar_compra(total_carrinho, usuario_logado)
        mostrar_menu_confirmar_compra()

        confirmar = ler_numero(
            "int",
            "Escolha uma opção: ",
            lambda: mostrar_tela_confirmar_compra(total_carrinho, usuario_logado),
        )

        if confirmar == 0:
            print("❌ Compra cancelada!")
            print("O carrinho foi mantido.")
            pausa()
            break

        if confirmar != 1:
            print("❌ Opção inválida! Escolha 1 ou 0.")
            pausa()
            continue

        # Valida existência e estoque antes de finalizar.
        for item in carrinho:
            nome, qtd, _ = item

            if nome not in produtos:
                print("❌ Não foi possível finalizar a compra!")
                print()
                print(f'O produto "{nome}" não existe mais no cadastro do mercado.')
                print()
                print("A compra foi cancelada.")
                print("O carrinho foi mantido para correção.")
                pausa()
                return

            if qtd > produtos[nome][1]:
                print("❌ Não foi possível finalizar a compra!")
                print()
                print(f"Estoque insuficiente para o produto: {nome}")
                print()
                print(f"Quantidade no carrinho: {qtd}")
                print(f"Estoque atual: {produtos[nome][1]}")
                print()
                print("A compra foi cancelada.")
                print("O carrinho foi mantido para correção.")
                pausa()
                return

        # Baixa o estoque de cada produto.
        for item in carrinho:
            nome, qtd, _ = item
            preco_atual, estoque_atual = produtos[nome]
            produtos[nome] = (preco_atual, estoque_atual - qtd)

        # Registra a venda unificada.
        vendas.append({
            "cliente": usuario_logado,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "itens": carrinho.copy(),
        })

        carrinho.clear()
        salvar_dados()

        print("✅ Compra finalizada com sucesso!")
        print()
        print("🧾 Obrigado pela preferência!")
        pausa()
        break


def relatorio_vendas() -> None:
    limpar_tela()
    print("📊 RELATÓRIO DE VENDAS")
    print()

    if not vendas:
        print("❌ Nenhuma venda realizada ainda!")
        pausa()
        return

    total_faturamento = 0.0

    for i, venda in enumerate(vendas, start=1):
        print(f"🧾 Venda {i}")
        print(f"👤 Cliente: {venda['cliente']}")
        print(f"📅 Data: {venda['data']}")
        print()

        total_venda = 0.0
        for j, item in enumerate(venda["itens"], start=1):
            nome, qtd, total_item = item
            print(f"{j} - {nome} | Quantidade: {qtd} | Total: R$ {total_item:.2f}")
            total_venda += total_item

        total_faturamento += total_venda

        print()
        print(f"💰 Total da venda: R$ {total_venda:.2f}")
        print("━" * 40)
        print()

    print(f"💵 FATURAMENTO TOTAL: R$ {total_faturamento:.2f}")
    pausa()


def limpar_dados() -> None:
    while True:
        mostrar_tela_limpar_dados()

        opcao = ler_numero("int", "Escolha uma opção: ", mostrar_tela_limpar_dados)

        if opcao == 0:
            print("❌ Operação cancelada!")
            print("Nenhum dado foi apagado.")
            pausa()
            break

        if opcao == 1:
            produtos.clear()

            for carrinho in carrinhos_usuarios.values():
                carrinho.clear()

            vendas.clear()
            salvar_dados()

            print("✅ Dados do mercado apagados com sucesso!")
            print()
            print("Produtos, estoques, carrinhos e vendas foram reiniciados.")
            print("Os usuários cadastrados foram mantidos.")
            pausa()
            break

        else:
            print("❌ Opção inválida! Escolha 1 ou 0.")
            pausa()


# ============================================================
# MENUS PRINCIPAIS DO SISTEMA
# ============================================================

def menu_admin() -> None:
    while True:
        mostrar_menu_admin()

        opcao = ler_numero("int", "Escolha uma opção: ", mostrar_menu_admin)

        if opcao == 1:
            cadastrar_produto()
        elif opcao == 2:
            listar_produtos()
        elif opcao == 3:
            editar_produtos()
        elif opcao == 4:
            relatorio_vendas()
        elif opcao == 5:
            limpar_dados()
        elif opcao == 0:
            print("👋 Saindo do painel do administrador...")
            print()
            print("↩️  Retornando ao menu inicial...")
            pausa()
            return
        else:
            print("❌ Opção inválida! Escolha uma opção do menu.")
            pausa()


def menu_cliente(usuario_logado: str) -> None:
    while True:
        mostrar_menu_cliente()

        opcao = ler_numero("int", "Escolha uma opção: ", mostrar_menu_cliente)

        if opcao == 1:
            listar_produtos_cliente(usuario_logado)
        elif opcao == 2:
            comprar_produtos(usuario_logado)
        elif opcao == 3:
            ver_carrinho(usuario_logado)
        elif opcao == 4:
            remover_item_carrinho(usuario_logado)
        elif opcao == 5:
            finalizar_compra(usuario_logado)
        elif opcao == 0:
            print("👋 Saindo do painel do cliente...")
            print()
            print("↩️  Retornando ao menu inicial...")
            pausa()
            return
        else:
            print("❌ Opção inválida! Escolha uma opção do menu.")
            pausa()


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":
    while True:
        mostrar_menu_inicial()

        opcao = ler_numero("int", "Escolha uma opção: ", mostrar_menu_inicial)

        if opcao == 0:
            print("👋 Saindo do sistema...")
            print("Obrigado por utilizar o Mercado Python!")
            break

        elif opcao == 1:
            fazer_login()

        elif opcao == 2:
            cadastrar_usuario()

        else:
            print("❌ Opção inválida! Escolha uma opção do menu.")
            pausa()
            limpar_tela()
