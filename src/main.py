# ============================================================
# ARQUIVO: src/main.py
# 
# DESCRIÇÃO:
#   - Ponto de entrada do programa. Controla o fluxo principal.
# 
# FUNÇÕES:
#   - main(): Função principal que inicializa o sistema.
#   - menu_principal(): Exibe opções de OPERAÇÃO (Buscar, Adicionar, Remover).
#   - escolher_chave(): Exibe opções de CHAVE (ID ou Nome).
#   - ler_dados_novo_filme(): Coleta os dados de um novo filme.
# 
# FLUXO DO MENU:
#   1. Carregar dados do CSV (leitura_csv.py).
#   2. Criar estruturas auxiliares (estruturas.py).
#   3. Loop do menu:
#      A) Usuário escolhe a OPERAÇÃO:
#         - Buscar
#         - Adicionar
#         - Remover
#         - Sair
#      B) Se escolher "Buscar":
#         - Usuário escolhe a CHAVE (ID ou Nome)
#         - Se ID: Chama busca sequencial + busca indexada
#         - Se Nome: Chama busca sequencial + busca hash
#      C) Se escolher "Adicionar":
#         - Coleta os dados do novo filme
#         - Atualiza todas as estruturas
#      D) Se escolher "Remover":
#         - Usuário escolhe a CHAVE (ID ou Nome)
#         - Se ID: Localiza com sequencial + indexada
#         - Se Nome: Localiza com sequencial + hash
#         - Atualiza todas as estruturas
# 
# OBSERVAÇÕES:
#   - Este módulo não contém lógica de busca.
#   - Apenas orquestra as chamadas às funções dos outros módulos.
# ============================================================