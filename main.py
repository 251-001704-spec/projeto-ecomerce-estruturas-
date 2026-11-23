"""
Projeto Final - Estruturas de Dados em Python
Tema 2: Plataforma de Comércio Eletrônico
Aluno: Patrick Braz Hespanhol | Matrícula: 251-001704

Estruturas utilizadas:
  - Lista  : catálogo de produtos ativos        (list)
  - Fila   : aprovação de pagamentos em ordem   (collections.deque)
  - Pilha  : histórico de navegação do cliente  (list, usando só o topo)
  - Árvore : departamentos > categorias > subcategorias (dicionários aninhados)

Persistência: arquivo texto único "dados_sistema.txt" (sem JSON/CSV/pickle).
"""

from collections import deque

ARQUIVO = "dados_sistema.txt"
SEP = "|"

# ---------------------------------------------------------------------------
# Estruturas em memória (o sistema inicia totalmente vazio)
# ---------------------------------------------------------------------------
catalogo = []            # Lista: cada item é {"id", "nome", "preco", "estoque"}
fila_pagamentos = deque()  # Fila: cada item é {"id", "cliente", "valor"}
pilha_navegacao = []     # Pilha: topo = último elemento; item {"pagina", "detalhe"}
arvore = {}              # Árvore: {"Departamento": {"Categoria": {"Subcategoria": {}}}}


# ---------------------------------------------------------------------------
# Utilitários de entrada
# ---------------------------------------------------------------------------
def ler_texto(mensagem):
    """Lê um texto não vazio e sem o delimitador '|' (para não quebrar o arquivo)."""
    while True:
        valor = input(mensagem).strip()
        if not valor:
            print("  Valor obrigatório.")
        elif SEP in valor:
            print(f"  O caractere '{SEP}' não é permitido.")
        else:
            return valor


def ler_inteiro(mensagem, minimo=0):
    while True:
        try:
            valor = int(input(mensagem).strip())
            if valor < minimo:
                print(f"  Informe um número maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("  Número inteiro inválido.")


def ler_decimal(mensagem):
    while True:
        try:
            valor = float(input(mensagem).strip().replace(",", "."))
            if valor < 0:
                print("  O valor não pode ser negativo.")
                continue
            return valor
        except ValueError:
            print("  Número inválido.")


def proximo_id(itens):
    """Gera o próximo id sequencial com base no maior id existente."""
    return max((item["id"] for item in itens), default=0) + 1


def buscar_por_id(itens, id_item):
    for item in itens:
        if item["id"] == id_item:
            return item
    return None


# ---------------------------------------------------------------------------
# LISTA - catálogo de produtos (acesso por id/índice)
# ---------------------------------------------------------------------------
def lista_inserir():
    produto = {
        "id": proximo_id(catalogo),
        "nome": ler_texto("Nome do produto: "),
        "preco": ler_decimal("Preço (R$): "),
        "estoque": ler_inteiro("Estoque: "),
    }
    catalogo.append(produto)
    print(f"Produto {produto['id']} cadastrado.")


def lista_listar():
    if not catalogo:
        print("Catálogo vazio.")
        return
    print(f"{'ID':<5}{'Produto':<30}{'Preço':>12}{'Estoque':>9}")
    for p in catalogo:
        print(f"{p['id']:<5}{p['nome']:<30}{p['preco']:>12.2f}{p['estoque']:>9}")


def lista_atualizar():
    produto = buscar_por_id(catalogo, ler_inteiro("ID do produto: "))
    if produto is None:
        print("Produto não encontrado.")
        return
    produto["nome"] = ler_texto(f"Novo nome [{produto['nome']}]: ")
    produto["preco"] = ler_decimal(f"Novo preço [{produto['preco']:.2f}]: ")
    produto["estoque"] = ler_inteiro(f"Novo estoque [{produto['estoque']}]: ")
    print("Produto atualizado.")


def lista_remover():
    produto = buscar_por_id(catalogo, ler_inteiro("ID do produto: "))
    if produto is None:
        print("Produto não encontrado.")
        return
    catalogo.remove(produto)
    print("Produto removido do catálogo.")


# ---------------------------------------------------------------------------
# FILA - pagamentos (entra no fim, sai do início: FIFO)
# ---------------------------------------------------------------------------
def fila_enfileirar():
    pedido = {
        "id": proximo_id(fila_pagamentos),
        "cliente": ler_texto("Nome do cliente: "),
        "valor": ler_decimal("Valor do pagamento (R$): "),
    }
    fila_pagamentos.append(pedido)  # inserção sempre no fim
    print(f"Pagamento do pedido {pedido['id']} entrou na fila.")


def fila_listar():
    if not fila_pagamentos:
        print("Fila de pagamentos vazia.")
        return
    print("Ordem de processamento (1º = próximo a ser aprovado):")
    for posicao, p in enumerate(fila_pagamentos, start=1):
        print(f"  {posicao}º | Pedido {p['id']} | {p['cliente']} | R$ {p['valor']:.2f}")


def fila_atualizar():
    """Altera os dados de um pedido sem mudar a posição dele na fila."""
    pedido = buscar_por_id(fila_pagamentos, ler_inteiro("ID do pedido: "))
    if pedido is None:
        print("Pedido não encontrado.")
        return
    pedido["cliente"] = ler_texto(f"Novo cliente [{pedido['cliente']}]: ")
    pedido["valor"] = ler_decimal(f"Novo valor [{pedido['valor']:.2f}]: ")
    print("Pedido atualizado.")


def fila_processar():
    """Remove e aprova o pagamento do início da fila."""
    if not fila_pagamentos:
        print("Fila de pagamentos vazia.")
        return
    p = fila_pagamentos.popleft()  # remoção sempre no início
    print(f"Pagamento aprovado: pedido {p['id']} de {p['cliente']} (R$ {p['valor']:.2f}).")


# ---------------------------------------------------------------------------
# PILHA - histórico de navegação (LIFO: tudo acontece no topo)
# ---------------------------------------------------------------------------
def pilha_empilhar():
    pilha_navegacao.append({
        "pagina": ler_texto("Página visitada: "),
        "detalhe": ler_texto("Detalhe (ex.: produto ou busca): "),
    })
    print("Página empilhada no histórico.")


def pilha_consultar():
    if not pilha_navegacao:
        print("Histórico de navegação vazio.")
        return
    print("Histórico (topo = página atual):")
    for posicao, item in enumerate(reversed(pilha_navegacao)):
        marca = "TOPO" if posicao == 0 else "    "
        print(f"  [{marca}] {item['pagina']} - {item['detalhe']}")


def pilha_atualizar_topo():
    if not pilha_navegacao:
        print("Histórico de navegação vazio.")
        return
    topo = pilha_navegacao[-1]
    topo["pagina"] = ler_texto(f"Nova página [{topo['pagina']}]: ")
    topo["detalhe"] = ler_texto(f"Novo detalhe [{topo['detalhe']}]: ")
    print("Topo atualizado.")


def pilha_desempilhar():
    """Voltar uma página: remove o topo."""
    if not pilha_navegacao:
        print("Histórico de navegação vazio.")
        return
    item = pilha_navegacao.pop()
    print(f"Voltando... removido: {item['pagina']} - {item['detalhe']}")


# ---------------------------------------------------------------------------
# ÁRVORE - departamentos > categorias > subcategorias (dicts aninhados)
# ---------------------------------------------------------------------------
def navegar(caminho):
    """
    Recebe um caminho como 'Eletrônicos > Celulares' e devolve o dicionário
    do nó correspondente. Caminho vazio = raiz. Retorna None se não existir.
    """
    no = arvore
    for parte in [p.strip() for p in caminho.split(">") if p.strip()]:
        if parte not in no:
            return None
        no = no[parte]
    return no


def separar_caminho(caminho):
    return [p.strip() for p in caminho.split(">") if p.strip()]


def arvore_inserir():
    caminho_pai = input("Caminho do pai (ex.: Eletrônicos > Celulares; vazio = raiz): ")
    pai = navegar(caminho_pai)
    if pai is None:
        print("Caminho do pai não encontrado.")
        return
    nome = ler_texto("Nome do novo nó: ")
    if nome in pai:
        print("Já existe um nó com esse nome nesse local.")
        return
    pai[nome] = {}
    print("Nó inserido.")


def imprimir_arvore(no, nivel=0):
    """Percorre recursivamente a árvore imprimindo com indentação."""
    for nome, filhos in no.items():
        print("  " * nivel + "- " + nome)
        imprimir_arvore(filhos, nivel + 1)


def arvore_listar():
    if not arvore:
        print("Árvore de categorias vazia.")
        return
    imprimir_arvore(arvore)


def arvore_atualizar():
    """Renomeia um nó mantendo seus filhos e sua posição."""
    partes = separar_caminho(input("Caminho do nó a renomear (ex.: Eletrônicos > Celulares): "))
    if not partes:
        print("Caminho inválido.")
        return
    pai = navegar(" > ".join(partes[:-1]))
    if pai is None or partes[-1] not in pai:
        print("Nó não encontrado.")
        return
    novo = ler_texto("Novo nome: ")
    if novo in pai and novo != partes[-1]:
        print("Já existe um nó com esse nome nesse local.")
        return
    itens = [(novo if k == partes[-1] else k, v) for k, v in pai.items()]
    pai.clear()
    pai.update(itens)
    print("Nó renomeado.")


def arvore_remover():
    """Remove um nó e toda a sua subárvore."""
    partes = separar_caminho(input("Caminho do nó a remover (ex.: Eletrônicos > Celulares): "))
    if not partes:
        print("Caminho inválido.")
        return
    pai = navegar(" > ".join(partes[:-1]))
    if pai is None or partes[-1] not in pai:
        print("Nó não encontrado.")
        return
    del pai[partes[-1]]
    print("Nó (e seus filhos) removido.")


def caminhos_folhas(no, prefixo=()):
    """Gera o caminho completo de cada folha (usado para salvar a árvore)."""
    for nome, filhos in no.items():
        caminho = prefixo + (nome,)
        if filhos:
            yield from caminhos_folhas(filhos, caminho)
        else:
            yield caminho


# ---------------------------------------------------------------------------
# PERSISTÊNCIA em dados_sistema.txt
#   LISTA|id|nome|preco|estoque
#   FILA|id|cliente|valor
#   PILHA|pagina|detalhe          (da base para o topo)
#   ARVORE|departamento|categoria|subcategoria...
# ---------------------------------------------------------------------------
def salvar_dados():
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as arq:
            for p in catalogo:
                arq.write(SEP.join(["LISTA", str(p["id"]), p["nome"], f"{p['preco']:.2f}", str(p["estoque"])]) + "\n")
            for p in fila_pagamentos:  # do início ao fim da fila
                arq.write(SEP.join(["FILA", str(p["id"]), p["cliente"], f"{p['valor']:.2f}"]) + "\n")
            for item in pilha_navegacao:  # da base ao topo
                arq.write(SEP.join(["PILHA", item["pagina"], item["detalhe"]]) + "\n")
            for caminho in caminhos_folhas(arvore):
                arq.write(SEP.join(["ARVORE", *caminho]) + "\n")
        print(f"Dados salvos em {ARQUIVO}.")
    except OSError as erro:
        print(f"Erro ao salvar: {erro}")


def carregar_dados():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arq:
            linhas = arq.read().splitlines()
    except FileNotFoundError:
        print(f"Arquivo {ARQUIVO} não encontrado. Salve os dados primeiro.")
        return
    except OSError as erro:
        print(f"Erro ao carregar: {erro}")
        return

    # Reconstrói tudo do zero a partir do disco
    catalogo.clear()
    fila_pagamentos.clear()
    pilha_navegacao.clear()
    arvore.clear()
    ignoradas = 0

    for linha in linhas:
        if not linha.strip():
            continue
        campos = linha.split(SEP)
        tipo = campos[0]
        try:
            if tipo == "LISTA":
                catalogo.append({"id": int(campos[1]), "nome": campos[2],
                                 "preco": float(campos[3]), "estoque": int(campos[4])})
            elif tipo == "FILA":
                fila_pagamentos.append({"id": int(campos[1]), "cliente": campos[2],
                                        "valor": float(campos[3])})
            elif tipo == "PILHA":
                pilha_navegacao.append({"pagina": campos[1], "detalhe": campos[2]})
            elif tipo == "ARVORE":
                no = arvore
                for nome in campos[1:]:
                    no = no.setdefault(nome, {})  # cria o nível se não existir
            else:
                ignoradas += 1
        except (IndexError, ValueError):
            ignoradas += 1

    print("Dados carregados.")
    if ignoradas:
        print(f"Aviso: {ignoradas} linha(s) inválida(s) ignorada(s).")


# ---------------------------------------------------------------------------
# MENUS
# ---------------------------------------------------------------------------
def submenu(titulo, opcoes):
    """Exibe um submenu e executa a função da opção escolhida até o usuário voltar."""
    while True:
        print(f"\n=== {titulo} ===")
        for numero, (rotulo, _) in enumerate(opcoes, start=1):
            print(f"{numero} - {rotulo}")
        print("0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha == "0":
            return
        if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
            opcoes[int(escolha) - 1][1]()
        else:
            print("Opção inválida.")


def menu_lista():
    submenu("CATÁLOGO DE PRODUTOS (Lista)", [
        ("Inserir produto", lista_inserir),
        ("Listar produtos", lista_listar),
        ("Atualizar produto", lista_atualizar),
        ("Remover produto", lista_remover),
    ])


def menu_fila():
    submenu("FILA DE PAGAMENTOS (Fila)", [
        ("Enfileirar pagamento (fim)", fila_enfileirar),
        ("Listar fila", fila_listar),
        ("Atualizar pedido", fila_atualizar),
        ("Processar próximo pagamento (início)", fila_processar),
    ])


def menu_pilha():
    submenu("HISTÓRICO DE NAVEGAÇÃO (Pilha)", [
        ("Empilhar página (topo)", pilha_empilhar),
        ("Consultar histórico", pilha_consultar),
        ("Atualizar topo", pilha_atualizar_topo),
        ("Desempilhar / voltar (topo)", pilha_desempilhar),
    ])


def menu_arvore():
    submenu("DEPARTAMENTOS E CATEGORIAS (Árvore)", [
        ("Inserir nó", arvore_inserir),
        ("Listar árvore", arvore_listar),
        ("Renomear nó", arvore_atualizar),
        ("Remover nó", arvore_remover),
    ])


def menu_principal():
    while True:
        print("\n===== E-COMMERCE - MENU PRINCIPAL =====")
        print("1 - Catálogo de produtos (Lista)")
        print("2 - Fila de pagamentos (Fila)")
        print("3 - Histórico de navegação (Pilha)")
        print("4 - Departamentos e categorias (Árvore)")
        print("5 - Salvar dados")
        print("6 - Carregar dados")
        print("0 - Sair")
        escolha = input("Opção: ").strip()
        if escolha == "1":
            menu_lista()
        elif escolha == "2":
            menu_fila()
        elif escolha == "3":
            menu_pilha()
        elif escolha == "4":
            menu_arvore()
        elif escolha == "5":
            salvar_dados()
        elif escolha == "6":
            carregar_dados()
        elif escolha == "0":
            print("Encerrando. Dados não salvos serão perdidos.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_principal()
