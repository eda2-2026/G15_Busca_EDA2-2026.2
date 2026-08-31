# ============================================================
# ARQUIVO: src/busca_hash.py
# 
# DESCRIÇÃO:
#   - Implementa a busca por hashing usando um dicionário Python.
# 
# FUNÇÕES:
#   - criar_hash_titulos(filmes): Cria dicionário com títulos normalizados.
#   - buscar_por_hash_titulos(hash_titulos, nome_busca): Busca no dicionário.
# 
# ALGORITMO:
#   - Normaliza o título (remove acentos, espaços, minúsculas).
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

import unicodedata


def normalizar_titulo(titulo):
    """
    Normaliza o título para ser utilizado como chave da tabela hash.

    Remove:
    - acentos;
    - espaços extras;
    - diferenças entre maiúsculas e minúsculas.
    """

    titulo = titulo.strip().lower()

    titulo = unicodedata.normalize('NFD', titulo)

    titulo = ''.join(
        caractere
        for caractere in titulo
        if unicodedata.category(caractere) != 'Mn'
    )

    return titulo


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