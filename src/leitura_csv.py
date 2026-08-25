# ============================================================
# ARQUIVO: src/leitura_csv.py
# 
# DESCRIÇÃO:
#   - Módulo responsável pela interface com o arquivo CSV.
# 
# FUNÇÕES:
#   - carregar_csv(caminho): 
#       Lê o arquivo CSV e retorna a lista de filmes (dicionários).
#   - salvar_csv(caminho, filmes): 
#       Escreve a lista de filmes de volta no CSV.
# 
# DETALHES DE IMPLEMENTAÇÃO:
#   - Utiliza csv.DictReader para ler (cada linha vira um dict).
#   - Utiliza csv.DictWriter para salvar.
#   - Trata automaticamente vírgulas e aspas nos campos.
#   - Cada dicionário contém TODAS as colunas do CSV, permitindo
#     que as funções de busca retornem informações completas.
# 
# OBSERVAÇÕES:
#   - Mantém a ordem original das linhas do CSV.
#   - Toda leitura é feita apenas no início do programa.
# ============================================================