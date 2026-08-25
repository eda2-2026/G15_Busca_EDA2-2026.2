import time
from pathlib import Path
from testId import criar_lista_ordenada


caminho_csv = Path(__file__).parent.parent / "filmes.csv"

inicio = time.perf_counter()

ids = criar_lista_ordenada(caminho_csv)

fim = time.perf_counter()

# print(ids)
print(f"Quantidade de IDs: {len(ids)}")
print(f"Tempo de execução: {fim - inicio:.6f} segundos")

ids_esperados = set(range(7081))
ids_encontrados = set(ids)

ids_faltantes = sorted(ids_esperados - ids_encontrados)

print(f"Quantidade de IDs: {len(ids)}")
print(f"IDs faltantes: {len(ids_faltantes)}")
print(f"IDs faltantes: {ids_faltantes}")