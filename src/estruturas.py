# Funções para criar/atualizar as estruturas# ============================================================
# ARQUIVO: src/estruturas.py
# 
# DESCRIÇÃO:
#   - Módulo responsável por criar e manter as estruturas
#     auxiliares que serão usadas pelos métodos de busca.
# 
# FUNÇÕES:
#   - criar_lista_ordenada(filmes): 
#       Cria uma cópia ordenada por ID da lista original.
#   - criar_indice(filmes_ordenados, tamanho_bloco): 
#       Cria o índice (lista de blocos) a partir da lista ordenada.
#   - criar_hash_nome(filmes): 
#       Cria o dicionário onde chave = título normalizado, valor = lista de filmes.
#   - atualizar_estruturas(filmes, filmes_ordenados, indice, hash_nome,
#                          novo_filme=None, id_remover=None): 
#       Sincroniza todas as estruturas após inserção/remoção.
# 
# DETALHES DE IMPLEMENTAÇÃO:
#   - A lista original (do CSV) NÃO é alterada.
#   - Todas as estruturas são criadas a partir dela, apenas com
#     referências aos mesmos dados (não são cópias duplicadas).
#   - Após adicionar/remover um filme, recomenda-se reconstruir
#     todas as estruturas do zero (por simplicidade, dado que o
#     conjunto tem ~7000 registros).
# 
# OBSERVAÇÕES:
#   - Este módulo não contém lógica de busca.
#   - Funciona como uma "fábrica" de estruturas de dados.
# ============================================================