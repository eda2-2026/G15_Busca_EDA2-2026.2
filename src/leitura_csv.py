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
#   - normalizar_titulo(titulo):
#       Normaliza um título (sem acento, minúsculo, sem espaços
#       extras) para uso como chave de comparação/busca. Usada
#       pela busca sequencial e pela busca por hash, para que
#       ambas retornem o mesmo conjunto de resultados.
# 
# DETALHES DE IMPLEMENTAÇÃO:
#   - Utiliza csv.reader para ler (cada linha vira uma lista).
#   - Utiliza csv.writer para salvar.
#   - Converte apenas 'id' e 'Ano de exibição' para inteiro.
#   - Demais campos permanecem como string.
# 
# OBSERVAÇÕES:
#   - Mantém a ordem original das linhas do CSV.
#   - Toda leitura é feita apenas no início do programa.
# ============================================================
import csv
import unicodedata

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


def normalizar_titulo(titulo):
    """
    Normaliza o título para ser utilizado como chave de comparação
    (busca sequencial) ou como chave da tabela hash (busca por hash).

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