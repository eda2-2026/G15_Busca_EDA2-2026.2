# ============================================================
# ARQUIVO: src/utils.py
# 
# DESCRIÇÃO:
#   - Funções utilitárias compartilhadas entre os módulos.
# 
# FUNÇÕES:
#   - normalizar_titulo(titulo): 
#       Normaliza um título (remove acentos, espaços extras e 
#       converte para minúsculas) para uso em buscas por nome.
#   - imprimir_filme(filme): 
#       Exibe um filme com TODAS as colunas do CSV.
#   - imprimir_lista_filmes(filmes): 
#       Exibe uma lista de filmes (usada quando há duplicatas).
#   - medir_tempo(funcao, *args): 
#       Mede o tempo de execução de uma função.
# 
# DETALHES:
#   - Usa unicodedata (biblioteca padrão) para remover acentos.
#   - Normalização é essencial para evitar problemas com 
#     maiúsculas, minúsculas, acentos e espaços extras.
# 
# OBSERVAÇÕES:
#   - Funções genéricas, reutilizáveis em vários contextos.
# ============================================================