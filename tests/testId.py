import csv
from pathlib import Path

def criar_lista_ordenada(caminho_csv):
    """
    Cria uma lista contendo os IDs dos filmes,
    ordenados de forma crescente.
    """

    ids = []

    with open(caminho_csv, "r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)

        # Ignora o cabeçalho
        next(leitor)

        for linha in leitor:
            ids.append(int(linha[0]))

    return sorted(ids)