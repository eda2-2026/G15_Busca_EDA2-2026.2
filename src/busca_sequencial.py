# ============================================================
# ARQUIVO: src/busca_sequencial.py
# 
# DESCRIÇÃO:
#   - Implementa a busca sequencial (ou linear) sem índice.
# 
# FUNÇÕES:
#   - buscar_por_id(filmes, id_busca): Busca por ID.
#   - buscar_por_nome(filmes, nome_busca): Busca por título.
# 
# ALGORITMO:
def criar_lista_ordenada(filmes):
    return sorted(filmes, key=lambda filme: filme["id"])

def busca_sequencial(lista, alvo):
    for i in range(len(lista)):     # - Percorre a lista original do início ao fim.
        if lista[i] == alvo:        # - Compara o campo especificado com o valor procurado.
            return i                # - Retorna o filme encontrado
    return -1                       # - Elemento não encontrado (colocar mensagem de falha)
#
# COMPLEXIDADE:
#   - Tempo: O(n) no pior caso.
#   - Espaço: O(1).
# 
# OBSERVAÇÕES:
#   - A lista não está ordenada (ordem do CSV).
#   - Busca por nome pode retornar múltiplos resultados.
# ============================================================

def buscar_por_id_sequencial():
    return

def buscar_por_nome_sequencial():
    return