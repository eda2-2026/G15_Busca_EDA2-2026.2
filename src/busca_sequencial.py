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
#   - Percorre a lista original do início ao fim.
#   - Compara o campo especificado com o valor procurado.
#   - Retorna o filme encontrado ou None.
# 
# COMPLEXIDADE:
#   - Tempo: O(n) no pior caso.
#   - Espaço: O(1).
# 
# OBSERVAÇÕES:
#   - A lista não está ordenada (ordem do CSV).
#   - Busca por nome pode retornar múltiplos resultados.
# ============================================================