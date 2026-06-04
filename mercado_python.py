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

# Este sistema foi desenvolvido em Python para simular um mercado pelo terminal.
# Ele possui dois tipos de usuário:
# - Administrador: cadastra produtos, edita estoque/preço, vê relatório e limpa dados.
# - Cliente: lista produtos, adiciona itens ao carrinho, remove itens e finaliza compras.
#
# Os dados são armazenados em dicionários e listas durante a execução.
# Para não perder os dados ao fechar o programa, o sistema usa JSON.
#
# Principais estruturas:
# - usuarios: guarda login, senha e tipo de usuário.
# - produtos: guarda preço e estoque dos produtos.
# - carrinhos_usuarios: guarda um carrinho separado para cada cliente.
# - vendas: guarda as compras finalizadas.
# - data_vendas: guarda a data e hora de cada venda.
# - clientes_vendas: guarda qual cliente fez cada compra.
#
# O programa principal fica dentro de:
# if __name__ == "__main__":
#
# Isso faz com que o menu principal só seja executado
# quando este arquivo for rodado diretamente.
#
# Se este arquivo for importado por outro código,
# as funções poderão ser usadas sem iniciar o menu automaticamente.
# ============================================================


# ============================================================
# IMPORTAÇÕES
# ============================================================

# O módulo os é usado para limpar a tela do terminal.
# No Windows, o comando usado é "cls"; em Linux/Mac, o comando é "clear".
import os

# datetime é usado para registrar o dia e o horário em que uma venda foi finalizada.
from datetime import datetime

# math é usado para validar números decimais.
# Com ele, o sistema bloqueia valores como "nan", "inf" e "-inf".
import math

# json é usado para salvar e carregar os dados do mercado em um arquivo.
# Isso permite que usuários, produtos, carrinhos e vendas continuem salvos
# mesmo depois de fechar o programa.
import json


# ============================================================
# DADOS GLOBAIS DO SISTEMA
# ============================================================
# Estes dicionários e listas ficam disponíveis para todo o programa.
# Eles funcionam como a memória do sistema enquanto o programa está rodando.
# O JSON serve para salvar essa memória em arquivo e recuperar depois.

# Guarda todos os usuários cadastrados.
# Estrutura:
# usuarios[nome_usuario] = [senha, tipo_usuario]
#
# Exemplo:
# usuarios["Davi"] = ["123", "cliente"]
# usuarios["Admin"] = ["123", "admin"]
usuarios = {}

# Guarda os produtos cadastrados no mercado.
# Estrutura usada no código:
# produtos[nome_produto] = (preco, estoque)
#
# Exemplo:
# produtos["Arroz"] = (15.0, 10)
#
# Observação sobre JSON:
# quando uma tupla é salva no JSON, ela volta como lista.
# Exemplo: (15.0, 10) pode voltar como [15.0, 10].
# Como o código acessa preço e estoque por índice [0] e [1], continua funcionando.
produtos = {}

# Guarda um carrinho separado para cada cliente.
# A chave é o nome do cliente, e o valor é a lista de itens do carrinho.
#
# Estrutura:
# carrinhos_usuarios[cliente] = [[produto, quantidade, total_do_item], ...]
#
# Exemplo:
# carrinhos_usuarios["Davi"] = [["Arroz", 2, 30.0]]
carrinhos_usuarios = {}

# Guarda todas as vendas finalizadas.
# Cada venda é uma cópia do carrinho no momento em que o cliente finaliza a compra.
vendas = []

# Guarda a data e a hora de cada venda.
# O índice desta lista acompanha o índice da lista vendas.
# Exemplo:
# vendas[0] pertence à data_vendas[0].
data_vendas = []

# Guarda o nome do cliente responsável por cada venda.
# O índice desta lista acompanha o índice da lista vendas.
# Exemplo:
# vendas[0] foi feita por clientes_vendas[0].
clientes_vendas = []


# ============================================================
# PERSISTÊNCIA DE DADOS COM JSON
# ============================================================
# Persistência significa manter os dados salvos mesmo depois que o programa fecha.
# Nesta versão, isso é feito com o arquivo "dados_mercado_python.json".
#
# Fluxo geral:
# 1. Quando o programa abre, carregar_dados() tenta ler o arquivo JSON.
# 2. Se o arquivo existir, os dados salvos voltam para os dicionários/listas.
# 3. Se o arquivo não existir ou estiver vazio/corrompido, o sistema começa vazio.
# 4. Sempre que alguma informação importante muda, salvar_dados() grava tudo no JSON.


# Nome do arquivo usado como banco de dados simples do sistema.
# Se quiser trocar o nome do arquivo JSON, basta alterar esta constante.
ARQUIVO_DADOS = "dados_mercado_python.json"


# Carrega os dados salvos no arquivo JSON.
# Se o arquivo ainda não existir, retorna a mesma estrutura vazia usada pelo sistema.
# Isso evita erro na primeira execução do programa.
def carregar_dados():

    try:
        # Abre o arquivo em modo leitura ("r") e lê seu conteúdo como JSON.
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except (FileNotFoundError, json.JSONDecodeError):
        # FileNotFoundError: acontece quando o arquivo JSON ainda não foi criado.
        # json.JSONDecodeError: acontece se o arquivo existir, mas estiver vazio ou inválido.
        # Nos dois casos, o sistema começa com dados vazios.
        return {
            "usuarios": {},
            "produtos": {},
            "carrinhos_usuarios": {},
            "vendas": [],
            "data_vendas": [],
            "clientes_vendas": []
        }


# Salva no JSON todos os dados importantes do sistema.
# Esta função deve ser chamada depois de qualquer alteração em usuários, produtos,
# carrinhos, vendas, datas ou clientes das vendas.
def salvar_dados():

    # Junta todos os dados globais em um único dicionário.
    # Esse dicionário é o que será transformado em JSON.
    dados = {
        "usuarios": usuarios,
        "produtos": produtos,
        "carrinhos_usuarios": carrinhos_usuarios,
        "vendas": vendas,
        "data_vendas": data_vendas,
        "clientes_vendas": clientes_vendas
    }

    # Abre o arquivo em modo escrita ("w").
    # Se o arquivo não existir, ele é criado.
    # Se já existir, ele é atualizado com os dados atuais.
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        # json.dump grava o dicionário dentro do arquivo.
        # indent=4 deixa o JSON organizado e fácil de ler.
        # ensure_ascii=False permite salvar acentos corretamente.
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


# Ao iniciar o programa, os dados salvos são carregados.
carregar_dados_salvos = carregar_dados()

# Depois de carregar o pacote do JSON, cada parte volta para sua variável original.
# Essas são as variáveis que o restante do programa usa.
usuarios = carregar_dados_salvos["usuarios"]
produtos = carregar_dados_salvos["produtos"]
carrinhos_usuarios = carregar_dados_salvos["carrinhos_usuarios"]
vendas = carregar_dados_salvos["vendas"]
data_vendas = carregar_dados_salvos["data_vendas"]
clientes_vendas = carregar_dados_salvos["clientes_vendas"]


# ============================================================
# FUNÇÕES AUXILIARES E TRATAMENTO DE ENTRADAS
# ============================================================

# Limpa a tela do terminal.
# Isso deixa o programa mais organizado visualmente entre uma tela e outra.
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


# Pausa o programa até o usuário pressionar ENTER.
# Essa função é usada para o usuário conseguir ler mensagens antes da tela mudar.
def pausa():
    print()
    input("Pressione ENTER para continuar...")


# Lê um número digitado pelo usuário e valida se ele é inteiro ou decimal.
#
# Parâmetros:
# tipo:
#   "int"   -> força a entrada a ser número inteiro.
#   "float" -> força a entrada a ser número decimal.
#
# mensagem:
#   texto que aparece no input().
#
# tela:
#   função opcional usada para redesenhar a tela depois de um erro.
#
# Exemplo de uso:
# ler_inteiro_ou_float("int", "Escolha uma opção: ")
# ler_inteiro_ou_float("float", "Preço: R$ ")
def ler_inteiro_ou_float(tipo, mensagem, tela=None):
    while True:

        if tipo == "int":
            try:
                # Tenta transformar a entrada em número inteiro.
                numero = int(input(mensagem))
                print()
                return numero

            except ValueError:
                # Se não conseguir transformar em inteiro, mostra erro.
                print()
                print("❌ Erro: digite um número válido!")
                pausa()

                # Se uma tela foi enviada, redesenha essa tela.
                # Caso contrário, apenas limpa o terminal.
                if tela != None:
                    tela()
                else:
                    limpar_tela()

        elif tipo == "float":
            try:
                # Troca vírgula por ponto para aceitar valores como "10,50".
                numero = float(input(mensagem).replace(",", "."))

                # Bloqueia valores especiais aceitos pelo Python,
                # mas inválidos para preço, como nan, inf e -inf.
                if not math.isfinite(numero):
                    raise ValueError

                print()
                return numero

            except ValueError:
                # Se não conseguir transformar em decimal, mostra erro.
                print()
                print("❌ Erro: digite um número válido!")
                pausa()

                if tela != None:
                    tela()
                else:
                    limpar_tela()

        else:
            # Esse erro só aconteceria se o programador chamasse a função errado.
            raise ValueError("Tipo inválido! Use 'int' ou 'float'.")


# Mostra as opções usadas quando ocorre erro no cadastro ou no login.
# O usuário pode tentar novamente ou voltar ao menu.
def mostrar_menu_erro():
    print()
    print("[1] Tentar novamente")
    print("[0] Voltar ao menu")
    print()


# Controla o menu de erro.
# Retorna 0 se o usuário quiser voltar.
# Retorna 1 se o usuário quiser tentar novamente.
def erro():
    while True:

        mostrar_menu_erro()

        opcao_erro = ler_inteiro_ou_float("int", "Escolha uma opção: ", mostrar_menu_erro)

        # Aceita apenas 0 ou 1.
        if opcao_erro in [0, 1]:
            limpar_tela()
            return opcao_erro

        else:
            print("❌ Opção inválida! Digite apenas 0 ou 1.")
            pausa()


# Converte a opção do menu de erro em True ou False.
# False significa voltar/sair.
# True significa tentar novamente.
def tratar_erro(opcao_erro):
    if opcao_erro == 0:
        return False

    elif opcao_erro == 1:
        return True


# ============================================================
# FUNÇÕES DE CÁLCULO
# ============================================================

# Calcula o estoque disponível de um produto para o cliente logado.
#
# Por que essa função existe?
# Porque o estoque disponível para o cliente não é apenas o estoque cadastrado.
# Também é preciso descontar o que esse cliente já colocou no próprio carrinho.
#
# Exemplo:
# Estoque cadastrado do Arroz = 10
# Cliente já colocou 2 Arroz no carrinho
# Estoque disponível para esse cliente = 8
def calcular_estoque_disponivel(nome_produto, usuario_logado):

    # Pega o carrinho do cliente que está logado.
    carrinho_usuario = carrinhos_usuarios[usuario_logado]

    # Pega o estoque total do produto cadastrado pelo administrador.
    estoque_produto = produtos[nome_produto][1]

    # Começa em 0 porque, no início, ainda não contamos nada no carrinho.
    quantidade_ja_no_carrinho = 0

    # Percorre os itens do carrinho.
    for i in range(len(carrinho_usuario)):

        # Se o item do carrinho for o produto procurado,
        # soma a quantidade já colocada no carrinho.
        if carrinho_usuario[i][0] == nome_produto:
            quantidade_ja_no_carrinho += carrinho_usuario[i][1]

    # Estoque disponível = estoque cadastrado - quantidade já reservada no carrinho.
    estoque_disponivel = estoque_produto - quantidade_ja_no_carrinho

    return estoque_disponivel


# ============================================================
# TELAS E MENUS PRINCIPAIS
# ============================================================

# Mostra o menu inicial do sistema.
# A partir dele o usuário pode fazer login, criar uma conta ou sair.
def mostrar_menu_inicial():
    limpar_tela()
    print("=" * 40)
    print("🛒 MERCADO PYTHON 🛒".center(40))
    print("=" * 40)
    print()
    print("[1] 🔐 Fazer Login")
    print("[2] 📝 Cadastrar Usuário")
    print("[0] 🚪 Sair")
    print()


# Mostra o painel do administrador.
# Esse menu aparece apenas para usuários cadastrados como "admin".
def mostrar_menu_admin():
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


# Mostra o painel do cliente.
# Esse menu aparece apenas para usuários cadastrados como "cliente".
def mostrar_menu_cliente():
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
# TELAS DE USUÁRIOS E LOGIN
# ============================================================

# Mostra a tela onde o usuário escolhe se será administrador ou cliente.
# Essa tela aparece depois de digitar e confirmar a senha no cadastro.
def mostrar_tela_tipo_usuario(cadastro_usuario):
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
# TELAS DE PRODUTOS E EDIÇÃO
# ============================================================

# Mostra o título da tela de cadastro de produto.
# É usado tanto no início do cadastro quanto quando a tela precisa ser redesenhada.
def mostrar_titulo_produto():
    limpar_tela()
    print("📦 CADASTRAR PRODUTO")
    print()


# Redesenha a tela durante o cadastro do preço.
# Mantém o nome do produto na tela para o usuário não se perder.
def mostrar_tela_preco_produto(nome_produto):
    mostrar_titulo_produto()
    print(f"Nome do produto: {nome_produto}")
    print()


# Redesenha a tela durante o cadastro da quantidade.
# Mantém nome e preço do produto para dar contexto ao usuário.
def mostrar_tela_quantidade_produto(nome_produto, preco_produto):
    mostrar_titulo_produto()
    print(f"Nome do produto: {nome_produto}")
    print()
    print(f"Preço do produto: R$ {preco_produto:.2f}")
    print()


# Mostra todos os produtos cadastrados para o administrador escolher qual editar.
def mostrar_tela_editar_produtos():
    limpar_tela()
    print("✏️  EDITAR PRODUTO")
    print()
    print("Produtos cadastrados:")
    print()

    contador = 0

    # Percorre o dicionário de produtos mostrando número, nome, preço e estoque.
    for (nome_produto, (preco_produto, quantidade_produto)) in produtos.items():
        print(f"{contador + 1} - {nome_produto} | R$ {preco_produto:.2f} | Estoque: {quantidade_produto}")
        contador += 1

    print()
    print("[0] Cancelar")
    print()


# Mostra as opções de edição para um produto já escolhido.
# O administrador pode alterar preço, alterar estoque total ou acrescentar estoque.
def mostrar_tela_opcoes_editar_produto(nome_produto):
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


# Mostra a tela usada nas opções de alterar estoque total e acrescentar estoque.
# O título muda de acordo com a operação.
def editar_produtos_alterar_estoque_ou_acrescentar(titulo, nome_produto):
    limpar_tela()
    print(titulo)
    print()
    print(f"📦 Produto: {nome_produto}")
    print(f"📦 Estoque atual: {produtos[nome_produto][1]}")
    print()


# Mostra a tela usada quando o administrador vai alterar o preço de um produto.
def editar_produtos_alterar_preco(nome_produto):
    limpar_tela()
    print("✏️  ALTERAR PREÇO")
    print()
    print(f"📦 Produto: {nome_produto}")
    print(f"💰 Preço atual: R$ {produtos[nome_produto][0]:.2f}")
    print()


# ============================================================
# TELAS DE COMPRA, CARRINHO E FINALIZAÇÃO
# ============================================================

# Mostra a tela de compra com os produtos disponíveis para o cliente logado.
# O estoque exibido considera o que o cliente já tem no carrinho.
def mostrar_titulo_comprar(usuario_logado):
    limpar_tela()
    print("🛒 COMPRAR PRODUTO")
    print()

    contador = 0

    for (nome_produto, (preco_produto, quantidade_produto)) in produtos.items():

        # Calcula o estoque real disponível para o cliente.
        estoque_disponivel = calcular_estoque_disponivel(nome_produto, usuario_logado)

        # Evita mostrar estoque negativo na tela.
        # Internamente, o sistema ainda usa estoque_disponivel para validar a compra.
        estoque_exibido = max(0, estoque_disponivel)

        print(f"{contador + 1} - {nome_produto} | R$ {preco_produto:.2f} | Estoque: {estoque_exibido}")
        contador += 1

    print()
    print("[0] Voltar ao menu")
    print()


# Mostra o produto escolhido antes de pedir a quantidade.
# Isso confirma para o cliente qual produto ele selecionou.
def mostrar_produto_escolhido(posicao_produto, estoque_disponivel):
    limpar_tela()
    print("🛒 COMPRAR PRODUTO")
    print()

    posicao_escolhida = posicao_produto
    contador = 0

    # Percorre os produtos até encontrar a posição escolhida.
    for (nome_produto, (preco_produto, quantidade_produto)) in produtos.items():
        if contador == posicao_escolhida:
            print(f"📦 Produto escolhido: {nome_produto}")
            print(f"💰 Preço unitário: R$ {preco_produto:.2f}")
            print(f"📦 Estoque disponível: {estoque_disponivel}")
            print()

        contador += 1


# Mostra o menu após adicionar um item ao carrinho.
# O cliente pode continuar comprando ou voltar ao painel.
def mostrar_menu_comprar_outro():
    print("Deseja comprar outro produto?")
    print()
    print("[1] Sim")
    print("[0] Voltar ao menu")
    print()


# Mostra os itens do carrinho para o cliente escolher qual remover.
def mostrar_tela_remover_item_carrinho(usuario_logado):

    carrinho_usuario = carrinhos_usuarios[usuario_logado]

    limpar_tela()
    print("🗑️  REMOVER ITEM DO CARRINHO")
    print()
    print("Itens no carrinho:")
    print()

    total = 0

    # Lista todos os itens do carrinho e calcula o total geral.
    for i in range(len(carrinho_usuario)):
        print(f"{i+1} - {carrinho_usuario[i][0]} | Quantidade: {carrinho_usuario[i][1]} | Total: R$ {carrinho_usuario[i][2]:.2f}")
        total += carrinho_usuario[i][2]

    print()
    print(f"💰 Total do carrinho: R$ {total:.2f}")
    print()
    print("[0] Cancelar")
    print()


# Mostra o menu depois que um item é removido.
# O cliente pode remover outro item ou voltar ao painel.
def mostrar_menu_remover_outro_item():
    print()
    print("Deseja remover outro item?")
    print()
    print("[1] Sim")
    print("[0] Voltar ao menu")
    print()


# Mostra o resumo da compra antes da confirmação final.
def mostrar_titulo_finalizar_compra(total_carrinho, usuario_logado):

    carrinho_usuario = carrinhos_usuarios[usuario_logado]

    limpar_tela()
    print("💳 FINALIZAR COMPRA")
    print()
    print("📦 Itens comprados:")
    print()

    # Lista todos os itens que serão comprados.
    for i in range(len(carrinho_usuario)):
        print(f"{i+1} - {carrinho_usuario[i][0]} | Quantidade: {carrinho_usuario[i][1]} | Total: R$ {carrinho_usuario[i][2]:.2f}")

    print()
    print("━" * 40)
    print()
    print(f"💰 Total da compra: R$ {total_carrinho:.2f}")
    print()


# Mostra as opções para confirmar ou cancelar a compra.
def mostrar_menu_confirmar_compra():
    print("Deseja confirmar a compra?")
    print()
    print("[1] Confirmar compra")
    print("[0] Cancelar")
    print()


# Junta o resumo da compra com o menu de confirmação.
# É usada como tela de redesenho quando o usuário digita uma opção inválida.
def mostrar_tela_confirmar_compra(total_carrinho, usuario_logado):
    mostrar_titulo_finalizar_compra(total_carrinho, usuario_logado)
    mostrar_menu_confirmar_compra()


# Mostra a tela de confirmação antes de limpar os dados do mercado.
# Essa confirmação evita que o administrador apague tudo sem querer.
def mostrar_tela_limpar_dados():
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

# Cadastra um novo usuário.
# O usuário pode ser administrador ou cliente.
# Se for cliente, o sistema também cria um carrinho vazio para ele.
def cadastrar_usuario():
    limpar_tela()

    while True:

        print("📝 CADASTRO 📝".center(40))
        print()

        # strip remove espaços no início/fim.
        # title padroniza visualmente o nome do usuário.
        cadastro_usuario = input("👤 Digite um usuário: ").strip().title()
        print()

        # Valida se o nome de usuário foi preenchido.
        if cadastro_usuario == "":
            print("❌ Usuário não pode ficar vazio!")

            opcao_erro = erro()
            acao = tratar_erro(opcao_erro)

            if acao == False:
                limpar_tela()
                break

            elif acao == True:
                limpar_tela()
                continue

        # Impede cadastrar dois usuários com o mesmo nome.
        elif cadastro_usuario in usuarios:
            print("❌ Usuário já cadastrado! Tente outro nome.")

            opcao_erro = erro()
            acao = tratar_erro(opcao_erro)

            if acao == False:
                limpar_tela()
                break

            elif acao == True:
                limpar_tela()
                continue

        else:
            # Pede a senha do novo usuário.
            cadastro_senha = input("🔒 Digite uma senha: ").strip()
            print()

            # Valida se a senha foi preenchida.
            if cadastro_senha == "":
                print("❌ Senha não pode ficar vazia!")

                opcao_erro = erro()
                acao = tratar_erro(opcao_erro)

                if acao == False:
                    limpar_tela()
                    break

                elif acao == True:
                    limpar_tela()
                    continue

            else:
                # Pede confirmação para evitar senha digitada errado.
                confirmacao_senha = input("Confirme sua senha: ").strip()
                print()

                if cadastro_senha == confirmacao_senha:

                    while True:

                        mostrar_tela_tipo_usuario(cadastro_usuario)

                        tipo_usuario = ler_inteiro_ou_float("int", 
                        "Escolha uma opção: ", 
                        lambda: mostrar_tela_tipo_usuario(cadastro_usuario))

                        # Cancela o cadastro antes de salvar o usuário.
                        if tipo_usuario == 0:
                            print("❌ Cadastro cancelado!")
                            print("Nenhum usuário foi salvo.")
                            pausa()
                            return

                        # Salva o usuário como administrador.
                        elif tipo_usuario == 1:
                            usuarios[cadastro_usuario] = [cadastro_senha, "admin"]

                            salvar_dados()

                            print("✅ Administrador cadastrado com sucesso!")
                            print("👉 Agora você já pode fazer login.")
                            pausa()
                            limpar_tela()
                            break

                        # Salva o usuário como cliente e cria um carrinho vazio para ele.
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

                else:
                    print("❌ As senhas não coincidem!")

                    opcao_erro = erro()
                    acao = tratar_erro(opcao_erro)

                    if acao == False:
                        limpar_tela()
                        break

                    elif acao == True:
                        limpar_tela()
                        continue


# Faz o login do usuário.
# Depois de validar senha e tipo de usuário, direciona para o painel correto.
def fazer_login():
    limpar_tela()

    while True:

        print("🔐 LOGIN 🔐".center(40))
        print()

        login_usuario = input("👤 Usuário: ").strip().title()

        # Verifica se o usuário existe no dicionário de usuários.
        if login_usuario in usuarios:
            login_senha = input("🔒 Senha: ").strip()

            senha_correta = usuarios[login_usuario][0]
            tipo_usuario = usuarios[login_usuario][1]

            # Se a senha estiver correta, entra no painel correspondente.
            if login_senha == senha_correta:

                if tipo_usuario == "admin":
                    print()
                    print("✅ Login realizado com sucesso!")
                    print()
                    print("🚀 Entrando no painel do administrador...")
                    pausa()
                    limpar_tela()
                    menu_admin()
                    break

                elif tipo_usuario == "cliente":
                    print()
                    print("✅ Login realizado com sucesso!")
                    print()
                    print("🚀 Entrando no painel do cliente...")
                    pausa()
                    limpar_tela()
                    menu_cliente(login_usuario)
                    break

            else:
                print()
                print("❌ Senha incorreta!")

                opcao_erro = erro()
                acao = tratar_erro(opcao_erro)

                if acao == False:
                    limpar_tela()
                    break

                elif acao == True:
                    limpar_tela()
                    continue

        else:
            print()
            print("❌ Usuário não cadastrado!")

            opcao_erro = erro()
            acao = tratar_erro(opcao_erro)

            if acao == False:
                limpar_tela()
                break

            elif acao == True:
                limpar_tela()
                continue


# ============================================================
# PRODUTOS E EDIÇÃO DE PRODUTOS
# ============================================================

# Cadastra um produto com nome, preço e quantidade em estoque.
# Essa função é acessada pelo painel do administrador.
def cadastrar_produto():
    limpar_tela()
    print("📦 CADASTRAR PRODUTO")
    print()

    # Cadastro do nome do produto.
    while True:
        nome_produto = input("Nome do produto: ").strip().title()
        print()

        # Não permite nome vazio.
        if nome_produto == "":
            print("❌ O nome do produto não pode ficar vazio!")
            pausa()
            mostrar_titulo_produto()
            continue

        # Não permite cadastrar produto repetido.
        elif nome_produto in produtos:
            print("❌ Produto já cadastrado! Digite outro nome.")
            pausa()
            mostrar_titulo_produto()
            continue

        else:
            break

    # Cadastro do preço do produto.
    while True:
        preco_produto = ler_inteiro_ou_float(
            "float",
            "Preço do produto: R$ ",
            lambda: mostrar_tela_preco_produto(nome_produto)
        )

        # Não permite preço negativo.
        if preco_produto < 0:
            print("❌ O preço não pode ser negativo!")
            pausa()
            mostrar_tela_preco_produto(nome_produto)
            continue

        # Não permite preço igual a zero.
        elif preco_produto == 0:
            print("❌ O preço deve ser maior que zero!")
            pausa()
            mostrar_tela_preco_produto(nome_produto)
            continue

        else:
            break

    # Cadastro da quantidade em estoque.
    while True:
        quantidade_produto = ler_inteiro_ou_float(
            "int",
            "Quantidade em estoque: ",
            lambda: mostrar_tela_quantidade_produto(nome_produto, preco_produto)
        )

        # Não permite estoque negativo.
        if quantidade_produto < 0:
            print("❌ A quantidade não pode ser negativa!")
            pausa()
            mostrar_tela_quantidade_produto(nome_produto, preco_produto)
            continue

        # Não permite cadastrar produto com estoque zero.
        elif quantidade_produto == 0:
            print("❌ A quantidade deve ser maior que zero!")
            pausa()
            mostrar_tela_quantidade_produto(nome_produto, preco_produto)
            continue

        else:
            break

    # Salva o produto no dicionário de produtos.
    produtos[nome_produto] = (preco_produto, quantidade_produto)

    salvar_dados()

    print("✅ Produto cadastrado com sucesso!")
    pausa()


# Lista produtos para o administrador.
# Aqui aparece o estoque total cadastrado, sem descontar carrinho de cliente.
def listar_produtos():
    limpar_tela()
    print("📋 LISTA DE PRODUTOS")
    print()

    if len(produtos) == 0:
        print("❌ Nenhum produto cadastrado!")
        pausa()

    else:
        contador = 0

        for (nome_produto, (preco_produto, quantidade_produto)) in produtos.items():
            print(f"{contador + 1} - {nome_produto} | R$ {preco_produto:.2f} | Estoque: {quantidade_produto}")
            contador += 1

        pausa()


# Lista produtos para o cliente.
# Aqui aparece o estoque disponível para compra, já descontando o carrinho do cliente.
def listar_produtos_cliente(usuario_logado):
    limpar_tela()
    print("📋 PRODUTOS DISPONÍVEIS PARA COMPRA")
    print()

    if len(produtos) == 0:
        print("❌ Nenhum produto cadastrado!")
        pausa()

    else:
        contador = 0

        for (nome_produto, (preco_produto, quantidade_produto)) in produtos.items():

            # Calcula o estoque disponível para esse cliente.
            estoque_disponivel = calcular_estoque_disponivel(nome_produto, usuario_logado)

            # Evita exibir números negativos na tela.
            estoque_exibido = max(0, estoque_disponivel)

            print(f"{contador + 1} - {nome_produto} | R$ {preco_produto:.2f} | Estoque: {estoque_exibido}")
            contador += 1

        pausa()


# Permite ao administrador editar os produtos cadastrados.
# É possível:
# 1. alterar preço;
# 2. alterar estoque total;
# 3. acrescentar quantidade ao estoque.
def editar_produtos():
    limpar_tela()

    # Cria uma lista com os nomes dos produtos para acessar pelo número escolhido.
    lista_produtos = list(produtos.keys())

    if len(lista_produtos) == 0:
        print("✏️  EDITAR PRODUTO")
        print()
        print("❌ Nenhum produto cadastrado para editar!")
        pausa()
        return

    else:
        while True:

            mostrar_tela_editar_produtos()

            opcao_editar_produtos = ler_inteiro_ou_float("int", "Escolha o número do produto que deseja editar: ", mostrar_tela_editar_produtos)

            if opcao_editar_produtos == 0:
                print("↩️  Saindo da edição do produto...")
                print()
                print("Retornando ao painel do administrador...")
                pausa()
                return

            elif opcao_editar_produtos < 0 or opcao_editar_produtos > len(lista_produtos):
                print("❌ Produto não encontrado! Escolha uma opção da lista.")
                pausa()
                continue

            # Converte a opção escolhida em índice de lista.
            opcao_editar_produtos -= 1
            nome_produto = lista_produtos[opcao_editar_produtos]

            while True:

                mostrar_tela_opcoes_editar_produto(nome_produto)

                opcao_desejada = ler_inteiro_ou_float("int", 
                "Escolha uma opção: ", 
                lambda: mostrar_tela_opcoes_editar_produto(nome_produto)
                )

                # Opção 1: altera o preço do produto.
                if opcao_desejada == 1:

                    preco_antigo = produtos[nome_produto][0]

                    while True:

                        editar_produtos_alterar_preco(nome_produto)

                        novo_preco = ler_inteiro_ou_float("float", 
                        "Novo preço: R$ ", 
                        lambda: editar_produtos_alterar_preco(nome_produto)
                        )

                        if novo_preco <= 0:
                            print("❌ O preço deve ser maior que zero!")
                            pausa()
                            continue

                        estoque_atual = produtos[nome_produto][1]
                        produtos[nome_produto] = (novo_preco, estoque_atual)

                        # Atualiza os carrinhos abertos dos clientes.
                        # Se algum cliente já tinha esse produto no carrinho,
                        # o total do item é recalculado com o novo preço.
                        for cliente in carrinhos_usuarios:
                            carrinho_cliente = carrinhos_usuarios[cliente]

                            for item in carrinho_cliente:
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

                # Opção 2: altera o estoque total do produto.
                elif opcao_desejada == 2:

                    estoque_antigo = produtos[nome_produto][1]

                    while True:

                        editar_produtos_alterar_estoque_ou_acrescentar("✏️  ALTERAR ESTOQUE TOTAL", nome_produto)

                        novo_estoque = ler_inteiro_ou_float("int", 
                        "Novo estoque total: ", 
                        lambda: editar_produtos_alterar_estoque_ou_acrescentar("✏️  ALTERAR ESTOQUE TOTAL", nome_produto)
                        )

                        if novo_estoque < 0:
                            print("❌ O estoque não pode ser negativo!")
                            pausa()
                            continue

                        preco_atual = produtos[nome_produto][0]
                        produtos[nome_produto] = (preco_atual, novo_estoque)

                        salvar_dados()

                        print("✅ Estoque atualizado com sucesso!")
                        print()
                        print(f"📦 Produto: {nome_produto}")
                        print(f"📦 Estoque antigo: {estoque_antigo}")
                        print(f"📦 Novo estoque: {novo_estoque}")
                        pausa()
                        break

                # Opção 3: acrescenta uma quantidade ao estoque atual.
                elif opcao_desejada == 3:

                    estoque_antigo = produtos[nome_produto][1]
                    preco_atual = produtos[nome_produto][0]

                    while True:

                        editar_produtos_alterar_estoque_ou_acrescentar("✏️  ACRESCENTAR ESTOQUE", nome_produto)

                        acrescentar_estoque = ler_inteiro_ou_float("int", 
                        "Quantidade para acrescentar: ", 
                        lambda: editar_produtos_alterar_estoque_ou_acrescentar("✏️  ACRESCENTAR ESTOQUE", nome_produto)
                        )

                        if acrescentar_estoque <= 0:
                            print("❌ A quantidade para acrescentar deve ser maior que zero!")
                            pausa()
                            continue

                        novo_estoque = estoque_antigo + acrescentar_estoque
                        produtos[nome_produto] = (preco_atual, novo_estoque)

                        salvar_dados()

                        print("✅ Estoque atualizado com sucesso!")
                        print()
                        print(f"📦 Produto: {nome_produto}")
                        print(f"📦 Estoque antigo: {estoque_antigo}")
                        print(f"➕ Quantidade adicionada: {acrescentar_estoque}")
                        print(f"📦 Novo estoque: {novo_estoque}")
                        pausa()
                        break

                elif opcao_desejada == 0:
                    print("↩️  Saindo da edição do produto...")
                    print()
                    print("Retornando ao painel do administrador...")
                    pausa()
                    return

                else:
                    print("❌ Opção inválida! Escolha 1, 2, 3 ou 0.")
                    pausa()
                    continue


# ============================================================
# COMPRA E CARRINHO
# ============================================================

# Permite ao cliente adicionar produtos ao próprio carrinho.
# O carrinho usado é sempre o carrinho do usuário logado.
def comprar_produtos(usuario_logado):

    carrinho_usuario = carrinhos_usuarios[usuario_logado]

    while True:
        limpar_tela()
        print("🛒 COMPRAR PRODUTO")
        print()

        if len(produtos) == 0:
            print("❌ Nenhum produto cadastrado para compra!")
            pausa()
            break

        else:
            contador = 0

            # Lista os produtos com o estoque disponível para esse cliente.
            for (nome_produto, (preco_produto, quantidade_produto)) in produtos.items():
                estoque_disponivel = calcular_estoque_disponivel(nome_produto, usuario_logado)
                estoque_exibido = max(0, estoque_disponivel)

                print(f"{contador + 1} - {nome_produto} | R$ {preco_produto:.2f} | Estoque: {estoque_exibido}")
                contador += 1

            print()
            print("[0] Voltar ao menu")
            print()

        # Escolha do produto.
        while True:
            escolha_produto = ler_inteiro_ou_float("int", 
            "Escolha o número do produto: ", 
            lambda: mostrar_titulo_comprar(usuario_logado))

            if escolha_produto == 0:
                return

            escolha_produto -= 1
            lista_produtos = list(produtos.keys())

            if escolha_produto < 0 or escolha_produto >= len(lista_produtos):
                print("❌ Produto não encontrado! Escolha uma opção da lista.")
                pausa()
                mostrar_titulo_comprar(usuario_logado)
                continue

            nome_produto_escolhido = lista_produtos[escolha_produto]
            preco_produto, estoque_produto = produtos[nome_produto_escolhido]
            estoque_disponivel = calcular_estoque_disponivel(nome_produto_escolhido, usuario_logado)

            if estoque_disponivel <= 0:
                print("❌ Esse produto está sem estoque no momento!")
                pausa()
                mostrar_titulo_comprar(usuario_logado)
                continue

            else:
                break

        mostrar_produto_escolhido(escolha_produto, estoque_disponivel)

        # Escolha da quantidade.
        while True:
            quantidade_produto_comprar = ler_inteiro_ou_float(
                "int",
                "Quantidade [0 para cancelar item]: ",
                lambda: mostrar_produto_escolhido(escolha_produto, estoque_disponivel)
            )

            if quantidade_produto_comprar == 0:
                break

            elif quantidade_produto_comprar <= 0:
                print("❌ A quantidade deve ser maior que zero!")
                pausa()
                mostrar_produto_escolhido(escolha_produto, estoque_disponivel)
                continue

            elif quantidade_produto_comprar > estoque_disponivel:
                print("❌ Estoque insuficiente!")
                print(f"Estoque disponível: {estoque_disponivel}")
                pausa()
                mostrar_produto_escolhido(escolha_produto, estoque_disponivel)
                continue

            else:
                break

        if quantidade_produto_comprar == 0:
            continue

        # Calcula o total do item escolhido.
        total = preco_produto * quantidade_produto_comprar

        # Controla se o produto já estava no carrinho.
        produto_ja_no_carrinho = False

        # Se o produto já existir no carrinho, soma quantidade e total.
        for i in range(len(carrinho_usuario)):
            if carrinho_usuario[i][0] == nome_produto_escolhido:
                carrinho_usuario[i][1] += quantidade_produto_comprar
                carrinho_usuario[i][2] += total

                produto_ja_no_carrinho = True
                break

        # Se o produto ainda não existir no carrinho, cria um novo item.
        if not produto_ja_no_carrinho:
            carrinho_usuario.append([nome_produto_escolhido, quantidade_produto_comprar, total])

        salvar_dados()    

        print("✅ Produto adicionado ao carrinho!")
        print()
        print(f"📦 Produto: {nome_produto_escolhido}")
        print(f"🔢 Quantidade: {quantidade_produto_comprar}")
        print(f"💰 Total: R$ {total:.2f}")
        print()

        # Pergunta se o cliente deseja comprar outro produto.
        while True:
            mostrar_menu_comprar_outro()

            opcao_comprar = ler_inteiro_ou_float("int", "Escolha uma opção: ", mostrar_menu_comprar_outro)

            if opcao_comprar == 1:
                limpar_tela()
                break

            elif opcao_comprar == 0:
                limpar_tela()
                break

            else:
                print("❌ Opção inválida! Escolha 1 ou 0.")
                pausa()
                print()
                continue

        if opcao_comprar == 0:
            break


# Mostra os itens do carrinho do cliente logado.
# Também calcula e exibe o total atual do carrinho.
def ver_carrinho(usuario_logado):

    carrinho_usuario = carrinhos_usuarios[usuario_logado]

    limpar_tela()
    print("🧺 CARRINHO")
    print()

    if len(carrinho_usuario) == 0:
        print("❌ Carrinho vazio!")
        pausa()

    else:
        total_carrinho = 0

        for i in range(len(carrinho_usuario)):
            print(f"{i+1} - {carrinho_usuario[i][0]} | Quantidade: {carrinho_usuario[i][1]} | Total: R$ {carrinho_usuario[i][2]:.2f}")
            total_carrinho = total_carrinho + carrinho_usuario[i][2]

        print()
        print(f"💰 Total do carrinho: R$ {total_carrinho:.2f}")

        pausa()


# Permite remover itens do carrinho do cliente logado.
# A remoção afeta apenas o carrinho do usuário atual.
def remover_item_carrinho(usuario_logado):

    carrinho_usuario = carrinhos_usuarios[usuario_logado]

    limpar_tela()
    print("🗑️  REMOVER ITEM DO CARRINHO")
    print()

    if len(carrinho_usuario) == 0:
        print("❌ Carrinho vazio! Não há itens para remover.")
        pausa()

    else:
        while True:

            mostrar_tela_remover_item_carrinho(usuario_logado)

            opcao_remover_item = ler_inteiro_ou_float(
                "int",
                "Escolha o número do item que deseja remover: ",
                lambda: mostrar_tela_remover_item_carrinho(usuario_logado)
            )

            if opcao_remover_item == 0:
                print("❌ Operação cancelada!")
                print("Nenhum item foi removido.")
                pausa()
                break

            else:
                # Converte a opção para índice da lista.
                opcao_remover_item -= 1

                if opcao_remover_item < 0 or opcao_remover_item >= len(carrinho_usuario):
                    print("❌ Item não encontrado! Escolha uma opção da lista.")
                    pausa()
                    continue

                else:
                    # Guarda os dados do item antes de remover,
                    # para exibir a confirmação ao usuário.
                    produto_removido = carrinho_usuario[opcao_remover_item][0]
                    quantidade_removida = carrinho_usuario[opcao_remover_item][1]
                    total_removido = carrinho_usuario[opcao_remover_item][2]

                    del carrinho_usuario[opcao_remover_item]

                    salvar_dados()

                    print("✅ Item removido do carrinho com sucesso!")
                    print()
                    print(f"📦 Produto removido: {produto_removido}")
                    print(f"🔢 Quantidade removida: {quantidade_removida}")
                    print(f"💰 Total removido: R$ {total_removido:.2f}")

                    if len(carrinho_usuario) == 0:
                        print()
                        print("❌ Carrinho vazio! Não há mais itens para remover.")
                        pausa()
                        break

                    else:
                        while True:

                            mostrar_menu_remover_outro_item()

                            remover_outro_item = ler_inteiro_ou_float(
                                "int",
                                "Escolha uma opção: ",
                                mostrar_menu_remover_outro_item
                            )

                            if remover_outro_item == 0:
                                print("↩️  Voltando ao menu principal...")
                                pausa()
                                return

                            elif remover_outro_item == 1:
                                break

                            else:
                                print("❌ Opção inválida! Escolha 1 ou 0.")
                                pausa()
                                continue


# ============================================================
# FINALIZAÇÃO, RELATÓRIO E LIMPEZA DE DADOS
# ============================================================

# Finaliza a compra do cliente logado.
# Essa função:
# - verifica se o carrinho não está vazio;
# - confirma se os produtos ainda existem;
# - verifica se ainda há estoque suficiente;
# - baixa o estoque;
# - registra a venda;
# - limpa o carrinho do cliente.
def finalizar_compra(usuario_logado):

    carrinho_usuario = carrinhos_usuarios[usuario_logado]

    limpar_tela()

    while True:

        print("💳 FINALIZAR COMPRA")
        print()

        if len(carrinho_usuario) == 0:
            print("❌ Carrinho vazio! Adicione produtos antes de finalizar a compra.")
            pausa()
            break

        else:
            total_carrinho = 0

            # Soma o total de todos os itens do carrinho.
            for i in range(len(carrinho_usuario)):
                total_carrinho += carrinho_usuario[i][2]

            mostrar_titulo_finalizar_compra(total_carrinho, usuario_logado)
            mostrar_menu_confirmar_compra()

            confirmar_compra = ler_inteiro_ou_float(
                "int",
                "Escolha uma opção: ",
                lambda: mostrar_tela_confirmar_compra(total_carrinho, usuario_logado)
            )

            if confirmar_compra == 1:

                # Antes de finalizar, verifica se os produtos ainda existem
                # e se o estoque ainda é suficiente.
                for i in range(len(carrinho_usuario)):
                    nome_do_produto = carrinho_usuario[i][0]

                    if nome_do_produto not in produtos:
                        print("❌ Não foi possível finalizar a compra!")
                        print()
                        print(f'O produto "{nome_do_produto}" não existe mais no cadastro do mercado.')
                        print()
                        print("A compra foi cancelada.")
                        print("O carrinho foi mantido para correção.")
                        pausa()
                        return

                    quantidade_do_produto = carrinho_usuario[i][1]
                    estoque_atual = produtos[nome_do_produto][1]

                    if quantidade_do_produto > estoque_atual:
                        print("❌ Não foi possível finalizar a compra!")
                        print()
                        print(f"Estoque insuficiente para o produto: {nome_do_produto}")
                        print()
                        print(f"Quantidade no carrinho: {quantidade_do_produto}")
                        print(f"Estoque atual: {estoque_atual}")
                        print()
                        print("A compra foi cancelada.")
                        print("O carrinho foi mantido para correção.")
                        pausa()
                        return

                # Depois da verificação, baixa o estoque de cada produto comprado.
                for i in range(len(carrinho_usuario)):
                    nome_do_produto = carrinho_usuario[i][0]
                    quantidade_do_produto = carrinho_usuario[i][1]

                    preco_atual = produtos[nome_do_produto][0]
                    estoque_atual = produtos[nome_do_produto][1]
                    novo_estoque = estoque_atual - quantidade_do_produto

                    produtos[nome_do_produto] = (preco_atual, novo_estoque)

                # Registra a data e a hora da venda.
                data_venda = datetime.now().strftime("%d/%m/%Y %H:%M")
                data_vendas.append(data_venda)

                # Salva uma cópia do carrinho como venda finalizada.
                vendas.append(carrinho_usuario.copy())

                # Limpa o carrinho do cliente após a compra.
                carrinho_usuario.clear()

                # Registra qual cliente fez a venda.
                clientes_vendas.append(usuario_logado)

                salvar_dados()

                print("✅ Compra finalizada com sucesso!")
                print()
                print("🧾 Obrigado pela preferência!")
                pausa()

                break

            elif confirmar_compra == 0:
                print("❌ Compra cancelada!")
                print("O carrinho foi mantido.")
                pausa()
                break

            else:
                print("❌ Opção inválida! Escolha 1 ou 0.")
                pausa()


# Mostra o relatório de vendas para o administrador.
# Exibe cada venda com cliente, data, produtos e total.
def relatorio_vendas():
    limpar_tela()
    print("📊 RELATÓRIO DE VENDAS")
    print()

    if len(vendas) == 0:
        print("❌ Nenhuma venda realizada ainda!")
        pausa()

    else:
        total_faturamento = 0

        # Percorre todas as vendas salvas.
        for i in range(len(vendas)):
            print(f"🧾 Venda {i+1}")
            print(f"👤 Cliente: {clientes_vendas[i]}")
            print(f"📅 Data: {data_vendas[i]}")
            print()

            total_venda = 0

            # Percorre os itens de uma venda específica.
            for j in range(len(vendas[i])):
                produto_relatorio = vendas[i][j][0]
                quantidade_relatorio = vendas[i][j][1]
                total_relatorio = vendas[i][j][2]

                print(f"{1+j} - {produto_relatorio} | Quantidade: {quantidade_relatorio} | Total: R$ {total_relatorio:.2f}")

                total_faturamento = total_faturamento + vendas[i][j][2]
                total_venda = total_venda + vendas[i][j][2]

            print()
            print(f"💰 Total da venda: R$ {total_venda:.2f}")
            print("━" * 40)
            print()

        print(f"💵 FATURAMENTO TOTAL: R$ {total_faturamento:.2f}")
        pausa()


# Limpa os dados do mercado mantendo os usuários cadastrados.
# São apagados:
# - produtos;
# - carrinhos;
# - vendas;
# - datas das vendas;
# - clientes das vendas.
def limpar_dados():

    while True:

        mostrar_tela_limpar_dados()

        opcao_limpar_dados = ler_inteiro_ou_float("int", "Escolha uma opção: ", mostrar_tela_limpar_dados)

        if opcao_limpar_dados == 0:
            print("❌ Operação cancelada!")
            print("Nenhum dado foi apagado.")
            pausa()
            break

        elif opcao_limpar_dados == 1:

            # Apaga todos os produtos cadastrados.
            produtos.clear()

            # Limpa o carrinho de cada cliente, mas mantém os usuários.
            for nome_cliente in carrinhos_usuarios:
                carrinhos_usuarios[nome_cliente].clear()

            # Apaga o histórico de vendas.
            vendas.clear()
            data_vendas.clear()
            clientes_vendas.clear()

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
            continue


# ============================================================
# MENUS PRINCIPAIS DO SISTEMA
# ============================================================

# Controla o painel do administrador após o login.
# Cada opção chama uma função específica do sistema.
def menu_admin():

    while True:

        mostrar_menu_admin()

        opcao_menu_admin = ler_inteiro_ou_float("int", "Escolha uma opção: ", mostrar_menu_admin)

        if opcao_menu_admin == 1:
            cadastrar_produto()

        elif opcao_menu_admin == 2:
            listar_produtos()

        elif opcao_menu_admin == 3:
            editar_produtos()

        elif opcao_menu_admin == 4:
            relatorio_vendas()

        elif opcao_menu_admin == 5:
            limpar_dados()

        elif opcao_menu_admin == 0:
            print("👋 Saindo do painel do administrador...")
            print()
            print("↩️  Retornando ao menu inicial...")
            pausa()
            return

        else:
            print("❌ Opção inválida! Escolha uma opção do menu.")
            pausa()


# Controla o painel do cliente após o login.
# O parâmetro usuario_logado é necessário para acessar o carrinho correto.
def menu_cliente(usuario_logado):

    while True:

        mostrar_menu_cliente()

        opcao_menu_cliente = ler_inteiro_ou_float("int", "Escolha uma opção: ", mostrar_menu_cliente)

        if opcao_menu_cliente == 1:
            listar_produtos_cliente(usuario_logado)

        elif opcao_menu_cliente == 2:
            comprar_produtos(usuario_logado)

        elif opcao_menu_cliente == 3:
            ver_carrinho(usuario_logado)

        elif opcao_menu_cliente == 4:
            remover_item_carrinho(usuario_logado)

        elif opcao_menu_cliente == 5:
            finalizar_compra(usuario_logado)

        elif opcao_menu_cliente == 0:
            print("👋 Saindo do painel do cliente...")
            print()
            print("↩️  Retornando ao menu inicial...")
            pausa()
            return

        else:
            print("❌ Opção inválida! Escolha uma opção do menu.")
            pausa()


# =========================
# PROGRAMA PRINCIPAL
# =========================

# Controla o menu inicial do sistema.
# Esta parte fica no final porque é onde o programa realmente começa a executar.
# Primeiro o usuário vê o menu inicial; o menu principal só aparece depois do login.
if __name__ == "__main__":

    while True:

        mostrar_menu_inicial()

        # Lê a opção escolhida no menu inicial.
        opcao = ler_inteiro_ou_float("int", "Escolha uma opção: ", mostrar_menu_inicial)

        # Encerra o sistema.
        if opcao == 0:
            print("👋 Saindo do sistema...")
            print("Obrigado por utilizar o Mercado Python!")
            break

        # Abre a tela de login.
        elif opcao == 1: 
            fazer_login()
            
        # Abre a tela de cadastro de usuário.
        elif opcao == 2: 
            cadastrar_usuario()
            
        # Tratamento para opção inválida.
        else:
            print("❌ Opção inválida! Escolha uma opção do menu.")
            pausa()
            limpar_tela()