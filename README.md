# Projeto Final – Estruturas de Dados (Tema 2: Plataforma de Comércio Eletrônico)

**Aluno:** Patrick Braz Hespanhol
**Matrícula:** 251-001704

Sistema em Python (terminal, menu numérico) que opera as quatro estruturas fundamentais — Lista, Fila, Pilha e Árvore — com persistência em arquivo texto.

## Como executar

Requisitos: Python 3.8 ou superior (apenas biblioteca padrão, nada para instalar).

```bash
python main.py
```

(Em alguns sistemas, use `python3 main.py`.)

O sistema inicia **vazio**. Use as opções do menu para cadastrar dados e, em seguida:

- **5 – Salvar dados**: grava o estado atual em `dados_sistema.txt` (criado na pasta de execução).
- **6 – Carregar dados**: reconstrói as estruturas em memória a partir de `dados_sistema.txt`.

Dados não salvos são perdidos ao sair.

## Estruturas e justificativa técnica

| Estrutura | Implementação | Papel no e-commerce |
|---|---|---|
| Lista | `list` | Catálogo de produtos ativos |
| Fila | `collections.deque` | Aprovação de pagamentos |
| Pilha | `list` (`append`/`pop`) | Histórico de navegação do cliente |
| Árvore | dicionários aninhados | Departamentos, categorias e subcategorias |

**Lista (catálogo).** O catálogo precisa de acesso, atualização e remoção de qualquer produto, não apenas das pontas, além de listagem completa. Uma lista permite percorrer e localizar itens por id/posição, com ordem de cadastro preservada.

**Fila (pagamentos).** Pagamentos devem ser aprovados na ordem de chegada (FIFO), por justiça e previsibilidade. A inserção ocorre no fim (`append`) e a remoção no início (`popleft`). Foi usado `deque` porque `popleft` é O(1), enquanto `list.pop(0)` é O(n).

**Pilha (histórico de navegação).** Voltar à página anterior é um comportamento LIFO: a última página visitada é a primeira a ser desfeita. Inserção, consulta do estado atual e remoção ocorrem sempre no topo, com `append` e `pop` em O(1) no fim da lista.

**Árvore (categorias).** Departamentos, categorias e subcategorias formam uma hierarquia de profundidade variável, em que cada nó pode ter vários filhos. Dicionários aninhados (`{"Eletrônicos": {"Celulares": {"Smartphones": {}}}}`) representam isso naturalmente, permitem busca de um filho por nome em O(1) e navegação por caminho (`Eletrônicos > Celulares`).

## Funcionalidades (CRUD)

| Estrutura | Criar | Ler | Atualizar | Deletar |
|---|---|---|---|---|
| Lista | Inserir produto | Listar | Atualizar por id | Remover por id |
| Fila | Enfileirar no fim | Listar na ordem | Atualizar pedido por id (posição mantida) | Processar o próximo (início) |
| Pilha | Empilhar no topo | Consultar (topo → base) | Atualizar o topo | Desempilhar o topo |
| Árvore | Inserir nó sob um caminho | Listar com indentação | Renomear nó | Remover nó e subárvore |

## Formato do arquivo `dados_sistema.txt`

Um único arquivo texto, uma linha por registro, campos separados por `|`, iniciando com o identificador da estrutura:

```
LISTA|1|Notebook|3500.50|5
FILA|1|Maria Souza|200.00
PILHA|Home|Pagina inicial
PILHA|Produto|Notebook
ARVORE|Eletronicos|Celulares|Smartphones
ARVORE|Eletronicos|Notebooks
```

- `LISTA|id|nome|preco|estoque`
- `FILA|id|cliente|valor` (da frente para o fim da fila)
- `PILHA|pagina|detalhe` (da base para o topo)
- `ARVORE|departamento|categoria|subcategoria...` (caminho completo até cada folha)

O caractere `|` é rejeitado nas entradas para não corromper o arquivo.
