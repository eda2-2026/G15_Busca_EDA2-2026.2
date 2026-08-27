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

import csv

def carregar_csv(caminho):
    filmes = []

    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            cabecalho = next(leitor)

            for linha in leitor:
                filme = dict(zip(cabecalho, linha))

                for chave, valor in filme.items():
                    if chave == 'id' or chave == 'Ano de exibição':
                        filme[chave] = int(valor)

                filmes.append(filme)

        print(f"{len(filmes)} filmes carregados!")
        return filmes
        
    except FileNotFoundError:
        print(f"Arquivo '{caminho}' não encontrado!")
        return []


def salvar_csv(caminho, filmes):
    if not filmes:
        print("Nenhum filme para salvar!")
        return False
    
    try:
        with open(caminho, 'w', newline='', encoding='utf-8') as arquivo:
            cabecalho = list(filmes[0].keys())
            escritor = csv.writer(arquivo)
            escritor.writerow(cabecalho)
            
            for filme in filmes:
                escritor.writerow([filme[col] for col in cabecalho])
        
        print(f"{len(filmes)} filmes salvos!")
        return True
    
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        return False
