# ============================================================
# ARQUIVO: tests/teste_desempenho.py
#
# DESCRIÇÃO:
#   - Mede o desempenho (tempo em ms e nº de comparações/
#     operações) de cada algoritmo de busca implementado no
#     projeto, para melhor caso, pior caso e caso médio.
#   - É este script que gerou os números da tabela de
#     "Resultados medidos" no README.md do projeto.
#
# METODOLOGIA:
#   - Cada medição repete a mesma busca várias vezes e tira a
#     média do tempo, para reduzir o ruído do cronômetro (uma
#     busca isolada dura microssegundos, tempo comparável à
#     precisão do próprio interpretador Python).
#   - O nº de repetições varia por teste: buscas muito rápidas
#     (indexada, hash) usam mais repetições; a sequencial por
#     título é usada com menos repetições, pois normaliza os
#     7.052 títulos a cada chamada e já é lenta sozinha.
#   - "Caso médio" usa uma amostra aleatória (seed fixa, para
#     reprodutibilidade) de IDs/títulos reais da base.
#   - "Melhor caso" e "pior caso" usam uma chave escolhida
#     propositalmente (ex.: primeiro elemento da lista, ou uma
#     chave inexistente) para forçar o comportamento esperado.
#
# COMO EXECUTAR:
#   python3 tests/teste_desempenho.py
#   (a partir da raiz do projeto, ou de dentro de tests/)
# ============================================================

import math
import os
import random
import statistics
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.leitura_csv import carregar_csv
from src.busca_sequencial import buscar_por_id_sequencial_comparacoes, buscar_por_nome_sequencial_comparacoes
from src.busca_indexada import construir_indice, buscar_por_id_comparacoes
from src.busca_hash import criar_hash_titulos, buscar_por_hash_titulos_operacoes

SEED = 7                  # fixa a amostragem aleatória, para resultados reprodutíveis
TAMANHO_AMOSTRA_ID = 60
TAMANHO_AMOSTRA_TITULO_RAPIDO = 40    # usado na busca por hash (barata)
TAMANHO_AMOSTRA_TITULO_LENTO = 15     # usado na busca sequencial por título (cara)

# --------------------------------------------------------
# UTILITÁRIO DE MEDIÇÃO
# --------------------------------------------------------
def medir_tempo_medio_ms(repeticoes, funcao, *args):
    """
    Executa `funcao(*args)` `repeticoes` vezes e retorna:
        (tempo_medio_em_ms, resultado_da_ultima_chamada)
    """
    inicio = time.perf_counter()
    for _ in range(repeticoes):
        resultado = funcao(*args)
    duracao_total_ms = (time.perf_counter() - inicio) * 1000
    return duracao_total_ms / repeticoes, resultado


def imprimir_linha(rotulo, tempo_ms, unidade_contagem, valor_contagem):
    print(f"  {rotulo:<38} {tempo_ms:>10.5f} ms   {valor_contagem:>6}  {unidade_contagem}")


# --------------------------------------------------------
# BUSCA POR ID (sequencial x indexada)
# --------------------------------------------------------
def testar_busca_por_id(filmes, blocos, indice):
    print("\n[ BUSCA POR ID — Sequencial x Indexada ]")
    print("  " + "-" * 66)

    primeiro_id = filmes[0]['id']
    id_inexistente = max(f['id'] for f in filmes) + 999

    random.seed(SEED)
    amostra_ids = random.sample([f['id'] for f in filmes], TAMANHO_AMOSTRA_ID)

    # --- sequencial ---
    t, (_, c) = medir_tempo_medio_ms(500, buscar_por_id_sequencial_comparacoes, filmes, primeiro_id)
    imprimir_linha("Sequencial — melhor caso (1º elem.)", t, "comparações", c)

    t, (_, c) = medir_tempo_medio_ms(500, buscar_por_id_sequencial_comparacoes, filmes, id_inexistente)
    imprimir_linha("Sequencial — pior caso (inexistente)", t, "comparações", c)

    tempos, comparacoes = [], []
    for id_busca in amostra_ids:
        t, (_, c) = medir_tempo_medio_ms(30, buscar_por_id_sequencial_comparacoes, filmes, id_busca)
        tempos.append(t)
        comparacoes.append(c)
    imprimir_linha(
        f"Sequencial — caso médio ({TAMANHO_AMOSTRA_ID} amostras)",
        statistics.mean(tempos), "comparações", round(statistics.mean(comparacoes), 1)
    )

    print()

    # --- indexada ---
    t, (_, c) = medir_tempo_medio_ms(500, buscar_por_id_comparacoes, blocos, indice, primeiro_id)
    imprimir_linha("Indexada — melhor caso (1º bloco)", t, "comparações", c)

    t, (_, c) = medir_tempo_medio_ms(500, buscar_por_id_comparacoes, blocos, indice, id_inexistente)
    imprimir_linha("Indexada — pior caso (último bloco)", t, "comparações", c)

    tempos, comparacoes = [], []
    for id_busca in amostra_ids:
        t, (_, c) = medir_tempo_medio_ms(30, buscar_por_id_comparacoes, blocos, indice, id_busca)
        tempos.append(t)
        comparacoes.append(c)
    imprimir_linha(
        f"Indexada — caso médio ({TAMANHO_AMOSTRA_ID} amostras)",
        statistics.mean(tempos), "comparações", round(statistics.mean(comparacoes), 1)
    )


# --------------------------------------------------------
# BUSCA POR TÍTULO (sequencial x hash)
# --------------------------------------------------------
def testar_busca_por_titulo(filmes, hash_titulos):
    print("\n[ BUSCA POR TÍTULO — Sequencial x Hash ]")
    print("  " + "-" * 66)

    primeiro_titulo = filmes[0]['Título da obra']
    titulo_inexistente = "Filme Que Nao Existe XYZ 123 Teste"

    random.seed(SEED)
    todos_titulos = [f['Título da obra'] for f in filmes]

    # --- sequencial (mais cara: normaliza os 7.052 títulos a cada chamada) ---
    t, (_, c) = medir_tempo_medio_ms(80, buscar_por_nome_sequencial_comparacoes, filmes, primeiro_titulo)
    imprimir_linha("Sequencial — 1º elemento", t, "comparações", c)

    t, (_, c) = medir_tempo_medio_ms(80, buscar_por_nome_sequencial_comparacoes, filmes, titulo_inexistente)
    imprimir_linha("Sequencial — inexistente", t, "comparações", c)

    amostra_lenta = random.sample(todos_titulos, TAMANHO_AMOSTRA_TITULO_LENTO)
    tempos, comparacoes = [], []
    for titulo in amostra_lenta:
        t, (_, c) = medir_tempo_medio_ms(15, buscar_por_nome_sequencial_comparacoes, filmes, titulo)
        tempos.append(t)
        comparacoes.append(c)
    imprimir_linha(
        f"Sequencial — caso médio ({TAMANHO_AMOSTRA_TITULO_LENTO} amostras)",
        statistics.mean(tempos), "comparações", round(statistics.mean(comparacoes), 1)
    )
    print("  (nota: sequencial por título sempre varre a lista inteira,")
    print("   pois pode haver mais de um filme com o mesmo título)")

    print()

    # --- hash ---
    t, (_, ops) = medir_tempo_medio_ms(500, buscar_por_hash_titulos_operacoes, hash_titulos, primeiro_titulo)
    imprimir_linha("Hash — melhor caso (sem colisão)", t, "operações", ops)

    t, (_, ops) = medir_tempo_medio_ms(500, buscar_por_hash_titulos_operacoes, hash_titulos, titulo_inexistente)
    imprimir_linha("Hash — chave inexistente", t, "operações", ops)

    amostra_rapida = random.sample(todos_titulos, TAMANHO_AMOSTRA_TITULO_RAPIDO)
    tempos, opss = [], []
    for titulo in amostra_rapida:
        t, (_, ops) = medir_tempo_medio_ms(20, buscar_por_hash_titulos_operacoes, hash_titulos, titulo)
        tempos.append(t)
        opss.append(ops)
    imprimir_linha(
        f"Hash — caso médio ({TAMANHO_AMOSTRA_TITULO_RAPIDO} amostras)",
        statistics.mean(tempos), "operações", round(statistics.mean(opss), 2)
    )

    # pior caso real: a última chave inserida no maior balde da tabela
    tamanhos_baldes = [len(balde) for balde in hash_titulos.baldes]
    indice_maior_balde = tamanhos_baldes.index(max(tamanhos_baldes))
    chave_no_fim_do_balde = hash_titulos.baldes[indice_maior_balde][-1][0]

    t, (_, ops) = medir_tempo_medio_ms(500, buscar_por_hash_titulos_operacoes, hash_titulos, chave_no_fim_do_balde)
    imprimir_linha(
        f"Hash — pior caso real (maior balde, {max(tamanhos_baldes)} itens)",
        t, "operações", ops
    )

    print()
    print(f"  Maior balde da tabela (colisões): {max(tamanhos_baldes)} itens")
    print(f"  Capacidade final da tabela: {hash_titulos.capacidade}")
    print(f"  Fator de carga final: {hash_titulos.quantidade_chaves / hash_titulos.capacidade:.3f}")


# --------------------------------------------------------
# EXECUÇÃO
# --------------------------------------------------------
if __name__ == "__main__":
    caminho_csv = os.path.join(os.path.dirname(__file__), '..', 'filmes.csv')
    filmes = carregar_csv(caminho_csv)

    if not filmes:
        print("[!] Não foi possível carregar 'filmes.csv'.")
        sys.exit(1)

    blocos, indice = construir_indice(filmes)
    hash_titulos = criar_hash_titulos(filmes)

    print("=" * 70)
    print("  TESTE DE DESEMPENHO — Sequencial x Indexada x Hash")
    print("=" * 70)
    print(f"  Total de filmes: {len(filmes)}")
    print(f"  Tamanho de bloco (indexada, √n): {int(math.sqrt(len(filmes)))}")
    print(f"  Número de blocos: {len(blocos)}")

    testar_busca_por_id(filmes, blocos, indice)
    testar_busca_por_titulo(filmes, hash_titulos)

    print("\n" + "=" * 70)
    print("  FIM DO TESTE DE DESEMPENHO")
    print("=" * 70)