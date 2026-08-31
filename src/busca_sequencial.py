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
#   - Busca por nome usa normalizar_titulo() (mesma normalização
#     de acentos/espaços/caixa usada na busca por hash), para que
#     os dois métodos retornem exatamente o mesmo conjunto de
#     resultados e a comparação de desempenho seja justa.
# ============================================================

from leitura_csv import normalizar_titulo

def criar_lista_ordenada(filmes):
    return sorted(filmes, key=lambda filme: filme["id"])


def buscar_por_id_sequencial(filmes, id_busca):
    for filme in filmes:
        if filme['id'] == id_busca:
            return filme
    return None


def buscar_por_nome_sequencial(filmes, nome_busca):
    resultados = []
    nome_normalizado = normalizar_titulo(nome_busca)
    
    for filme in filmes:
        titulo_normalizado = normalizar_titulo(filme['Título da obra'])
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

def buscar_por_nome_sequencial_comparacoes(filmes, nome_busca):
    """
    Busca filmes por título de forma sequencial,
    contabilizando o número de comparações realizadas.

    Retorna:
        resultados: lista de filmes encontrados
        comparacoes: quantidade de comparações realizadas
    """

    resultados = []
    comparacoes = 0

    nome_normalizado = normalizar_titulo(nome_busca)

    for filme in filmes:
        titulo_normalizado = normalizar_titulo(filme['Título da obra'])

        comparacoes += 1

        if titulo_normalizado == nome_normalizado:
            resultados.append(filme)

    return resultados, comparacoes