# ============================================================
# ARQUIVO: src/busca_hash.py
#
# DESCRIÇÃO:
#   - Implementa a busca por hashing usando um dicionário Python.
#
# FUNÇÕES:
#   - criar_hash_titulos(filmes): Cria dicionário com títulos normalizados.
#   - buscar_por_hash_titulos(hash_titulos, nome_busca):
#       Busca no dicionário.
#
# ALGORITMO:
#   - Normaliza o título (remove acentos, espaços, minúsculas) via
#     normalizar_titulo(), importada de leitura_csv.py.
#   - Usa o título como chave no dicionário.
#   - Se houver duplicatas, armazena uma lista de filmes.
#
# COMPLEXIDADE:
#   - Tempo: O(1) em média.
#   - Espaço: O(n) para armazenar o dicionário.
#
# OBSERVAÇÕES:
#   - Python implementa hashing internamente nos dicionários.
#   - A busca é eficiente, mas não mantém ordem dos elementos.
# ============================================================

from leitura_csv import normalizar_titulo


def criar_hash_titulos(filmes):
    """
    Cria a tabela hash dos filmes.

    Chave:
        título normalizado

    Valor:
        lista de filmes com aquele título
    """

    hash_titulos = {}

    for filme in filmes:
        titulo = filme['Título da obra']
        chave = normalizar_titulo(titulo)

        if chave not in hash_titulos:
            hash_titulos[chave] = []

        hash_titulos[chave].append(filme)

    return hash_titulos


def buscar_por_hash_titulos(hash_titulos, nome_busca):
    """
    Busca filmes pelo título utilizando a tabela hash.

    Retorna:
        lista de filmes encontrados
    """

    chave = normalizar_titulo(nome_busca)

    return hash_titulos.get(chave, [])


def buscar_por_hash_titulos_operacoes(hash_titulos, nome_busca):
    """
    Busca filmes pelo título utilizando a tabela hash
    e contabiliza a operação de consulta.

    Diferente da busca sequencial/indexada, o dict do Python não
    expõe comparações internas: o acesso é feito por cálculo de
    hash + lookup direto no slot (O(1) amortizado). Por isso aqui
    contamos "operações de acesso" (a consulta ao dicionário), e
    não "comparações" no sentido de percorrer/comparar elementos.

    Retorna:
        resultados: lista de filmes encontrados
        operacoes: quantidade de operações de acesso contabilizadas
    """

    chave = normalizar_titulo(nome_busca)

    operacoes = 1

    resultados = hash_titulos.get(chave, [])

    return resultados, operacoes