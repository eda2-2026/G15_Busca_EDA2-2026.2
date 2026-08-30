# ============================================================
# ARQUIVO: src/busca_sequencial.py
# 
# DESCRIÇÃO:
#   - Implementa a busca sequencial (ou linear) sem índice.
# 
# FUNÇÕES:
#   - criar_lista_ordenada(filmes): Ordena por ID.
#   - buscar_por_id_sequencial(filmes, id_busca): Busca por ID.
#   - buscar_por_nome_sequencial(filmes, nome_busca): Busca por título.
# 
# ALGORITMO:
#   1. Percorre a lista do início ao fim.
#   2. Compara o campo especificado com o valor procurado.
#   3. Retorna o filme encontrado ou None.
# 
# COMPLEXIDADE:
#   - Tempo: O(n) no pior caso.
#   - Espaço: O(1).
# 
# OBSERVAÇÕES:
#   - A lista não está ordenada (ordem do CSV).
#   - Busca por nome pode retornar múltiplos resultados.
#   - Case insensitive (não diferencia maiúsculas/minúsculas).
# ============================================================

def criar_lista_ordenada(filmes):
    return sorted(filmes, key=lambda filme: filme["id"])


def buscar_por_id_sequencial(filmes, id_busca):
    for filme in filmes:
        if filme['id'] == id_busca:
            return filme
    return None


def buscar_por_nome_sequencial(filmes, nome_busca):
    resultados = []
    nome_normalizado = nome_busca.strip().lower()
    
    for filme in filmes:
        titulo_normalizado = filme['Título da obra'].strip().lower()
        if titulo_normalizado == nome_normalizado:
            resultados.append(filme)
    
    return resultados

def buscar_por_id_sequencial_comparacoes(filmes, id_busca):
    comparacoes = 0
    
    for filme in filmes:
        comparacoes += 1
        if filme['id'] == id_busca:
            return filme, comparacoes
    
    return None, comparacoes