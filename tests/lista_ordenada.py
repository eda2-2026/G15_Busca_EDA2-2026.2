from src.leitura_csv import carregar_csv
from src.busca_sequencial import criar_lista_ordenada
import time
from pathlib import Path

# Teste da função criar_lista_ordenada integrada com carregar_csv

caminho_csv = Path(__file__).parent.parent / "filmes.csv"

inicio = time.perf_counter()

filmes = carregar_csv(caminho_csv)

fim = time.perf_counter()


filmes_ordenados = criar_lista_ordenada(filmes)

num = int(input("numeros de id: "))
print(f"Primeiros {num} IDs:")
for filme in filmes_ordenados[:num]:
    print(filme["id"])

print(type(filmes))
print(type(filmes[0]))
print(filmes[0])