# ============================================================
# ARQUIVO: src/busca_indexada.py
# 
# DESCRIÇÃO:
#   - Implementa la busca sequencial indexada (por ID).
# 
# FUNÇÕES:
#   - montar_indice(filmes_ordenados, tamanho_bloco): Cria o índice.
#   - buscar_por_id(filmes_ordenados, indice, id_busca): Busca usando índice.
# 
# ALGORITMO:
#   1. Cria um índice que aponta para blocos de filmes.
#   2. Na busca, determina o bloco onde o ID está.
#   3. Percorre apenas os elementos daquele bloco.
# 
# COMPLEXIDADE:
#   - Tempo: O(n/bloco) no pior caso.
#   - Espaço: O(n/bloco) para o índice.
# 
# OBSERVAÇÕES:
#   - Requer uma lista ordenada por ID (criada em estruturas.py).
#   - O índice é composto por pares (ID, posição).
# ============================================================

def montar_indice():
    return

def buscar_por_id_indexada():
    return