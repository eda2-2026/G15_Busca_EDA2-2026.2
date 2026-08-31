# ============================================================
# ARQUIVO: src/busca_indexada.py
# 
# DESCRIÇÃO:
#   - Implementa a busca sequencial indexada (por ID).
# 
# FUNÇÕES:
#   - construir_indice: Cria blocos e índice.
#   - buscar_por_id: Busca usando índice.
#   - inserir_filme: Insere no último bloco.
#   - excluir_filme: Remove e compacta.
#   - redistribuir: Reorganiza quando necessário.
# 
# ALGORITMO:
#   1. Divide a lista em blocos de tamanho √n.
#   2. Cria índice: primeiro ID de cada bloco → número do bloco.
#   3. Na busca, localiza o bloco pelo índice.
#   4. Percorre apenas os elementos daquele bloco.
# 
# COMPLEXIDADE:
#   - Busca: O(√n) no pior caso.
#   - Inserção: O(1) no último bloco, O(n) na redistribuição.
#   - Espaço: O(n) para blocos + O(√n) para índice.
# 
# OBSERVAÇÕES:
#   - Tamanho do bloco = √n (calculado dinamicamente).
#   - Apenas o último bloco possui espaços vazios.
#   - Redistribui quando o último bloco fica cheio.
#   - IDs originais do CSV são preservados.
# ============================================================
import math

def construir_indice(filmes):
    tamanho_bloco = int(math.sqrt(len(filmes)))

    blocos = []                                  
    indice = {}                 

    for i in range(0, len(filmes), tamanho_bloco):
        bloco = filmes[i:i + tamanho_bloco]
        numero_bloco = len(blocos)

        if i + tamanho_bloco >= len(filmes):
            while len(bloco) < tamanho_bloco:
                bloco.append(None)
            
        blocos.append(bloco)
        indice[bloco[0]['id']] = numero_bloco
    return blocos, indice

def buscar_por_id(blocos, indice, id_busca):
    bloco_alvo = -1

    for id_inicial, numero_bloco in indice.items():
        if id_busca >= id_inicial:
            bloco_alvo = numero_bloco
        else: 
            break

    if bloco_alvo == -1:
        return None

    for filme in blocos[bloco_alvo]:
        if filme and filme['id'] == id_busca:
            return filme
    return None

def buscar_por_id_comparacoes(blocos, indice, id_busca):
    comparacoes = 0
    bloco_alvo = -1

    for id_inicial, numero_bloco in indice.items():
        comparacoes += 1
        if id_busca >= id_inicial:
            bloco_alvo = numero_bloco
        else:
            break

    if bloco_alvo == -1:
        return None, comparacoes

    for filme in blocos[bloco_alvo]:
        comparacoes += 1
        if filme and filme['id'] == id_busca:
            return filme, comparacoes
        
    return None, comparacoes

def inserir_filme(blocos, indice, filme):
    existente = buscar_por_id(blocos, indice, filme['id'])
    if existente:
        return False

    ultimo_bloco = len(blocos) - 1

    for i, item in enumerate(blocos[ultimo_bloco]):
        if item is None:
            blocos[ultimo_bloco][i] = filme
            return True

    #se o ultimo bloco estiver cheio redistribui
    redistribuir(blocos,indice)
    return inserir_filme(blocos,indice,filme)

def excluir_filme(blocos, indice, id_excluir):
    for i, bloco in enumerate(blocos):
        for j, filme in enumerate(bloco):
            if filme and filme['id'] == id_excluir:
                blocos[i][j] = None

                filmes_existentes = [f for f in bloco if f is not None]
                bloco_novo = filmes_existentes + [None] * (len(bloco) - len(filmes_existentes))
                blocos[i] = bloco_novo

                return True
    return False

def redistribuir(blocos, indice):
    todos = []
    for bloco in blocos:
        for filme in bloco:
            if filme is not None:
                todos.append(filme)

    tamanho_bloco = int(math.sqrt(len(todos)))

    blocos.clear()
    indice.clear()

    for i in range(0, len(todos), tamanho_bloco):
        bloco = todos[i:i + tamanho_bloco]

        if i + tamanho_bloco >= len(todos):
            while len(bloco) < tamanho_bloco:
                bloco.append(None)

        indice[bloco[0]['id']] = len(blocos)
        blocos.append(bloco)