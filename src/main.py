# ============================================================
# ARQUIVO: src/main.py
# 
# DESCRIÇÃO:
#   - Ponto de entrada do programa. Controla o fluxo principal.
# 
# FUNÇÕES:
#   - main(): Função principal que inicializa o sistema.
#   - buscar_por_id(): Busca filme por ID (indexada + sequencial).
#   - buscar_por_nome(): Busca filme por nome (sequencial).
#   - inserir(): Adiciona novo filme (lista + indexada).
#   - excluir(): Remove filme por ID ou nome (lista + indexada).
#   - exibir_filme(): Mostra dados do filme formatados.
# 
# FLUXO DO MENU:
#   1. Carregar dados do CSV (leitura_csv.py).
#   2. Construir estruturas de busca (busca_indexada.py).
#   3. Loop do menu:
#      A) Usuário escolhe a OPERAÇÃO:
#         - Buscar
#         - Inserir
#         - Excluir
#         - Sair
#      B) Se escolher "Buscar":
#         - Usuário escolhe a CHAVE (ID ou Nome)
#         - Se ID: Chama busca indexada + busca sequencial
#         - Se Nome: Chama busca sequencial
#      C) Se escolher "Inserir":
#         - Coleta os dados do novo filme
#         - Adiciona na lista original e na indexada
#      D) Se escolher "Excluir":
#         - Usuário escolhe a CHAVE (ID ou Nome)
#         - Se ID: Remove da lista original e da indexada
#         - Se Nome: Lista opções e pergunta qual excluir
#      E) Se escolher "Sair":
#         - Pergunta se deseja salvar no CSV
# 
# OBSERVAÇÕES:
#   - Este módulo não contém lógica de busca.
#   - Apenas orquestra as chamadas às funções dos outros módulos.
#   - Compara tempo de execução entre estruturas.
# ============================================================
import sys
import os
import time

sys.path.append(os.path.dirname(__file__))

from leitura_csv import carregar_csv, salvar_csv
from busca_indexada import construir_indice, buscar_por_id_comparacoes, inserir_filme, excluir_filme
from busca_sequencial import buscar_por_nome_sequencial, buscar_por_id_sequencial_comparacoes, buscar_por_nome_sequencial_comparacoes
from busca_hash import criar_hash_titulos, buscar_por_hash_titulos_operacoes

def exibir_filme(filme):
    print(f"\n 🎥 Título: {filme['Título da obra']} ({filme['Ano de exibição']})")
    print(f"    ├─ ID......: {filme['id']}")
    print(f"    ├─ Gênero..: {filme['Gênero']}")
    print(f"    └─ País....: {filme['País(es) produtor(es) da obra']}")

def buscar_por_id(filmes, blocos, indice):
    print("\n ╭─ Busca por ID")
    try:
        id_busca = int(input(" ╰─❯ Digite o ID: "))
    except ValueError:
        print("\n [!] Erro: ID inválido!")
        return
    
    inicio = time.perf_counter()
    filme_idx, comps_idx = buscar_por_id_comparacoes(blocos, indice, id_busca)
    tempo_idx = (time.perf_counter() - inicio) * 1000
    
    inicio = time.perf_counter()
    filme_seq, comps_seq = buscar_por_id_sequencial_comparacoes(filmes, id_busca)
    tempo_seq = (time.perf_counter() - inicio) * 1000
    
    print("\n [ RESULTADOS DA BUSCA ]")
    print("  " + "-"*40)
    
    if filme_idx:
        print(f" • Indexada   : {tempo_idx:.3f} ms | {comps_idx:3d} comparações")
    else:
        print(f" • Indexada   : não encontrado | {comps_idx:3d} comparações")
    
    if filme_seq:
        print(f" • Sequencial : {tempo_seq:.3f} ms | {comps_seq:3d} comparações")
    else:
        print(f" • Sequencial : não encontrado | {comps_seq:3d} comparações")
    
    print("  " + "-"*40)
    
    if filme_idx or filme_seq:
        exibir_filme(filme_idx or filme_seq)

def buscar_por_nome(filmes, hash_titulos):
    print("\n ╭─ Busca por Título")
    nome = input(" ╰─❯ Digite o Título: ").strip()

    # Busca sequencial
    inicio = time.perf_counter()
    resultados_seq, comps_seq = buscar_por_nome_sequencial_comparacoes(filmes, nome)
    tempo_seq = (time.perf_counter() - inicio) * 1000

    # Busca por hash
    inicio = time.perf_counter()
    resultados_hash, ops_hash = buscar_por_hash_titulos_operacoes(hash_titulos, nome)
    tempo_hash = (time.perf_counter() - inicio) * 1000

    print("\n [ RESULTADOS DA BUSCA ]")
    print("  " + "-" * 50)

    print(f" • Hash       : {tempo_hash:.3f} ms | {ops_hash:3d} operações")
    print(f" • Sequencial : {tempo_seq:.3f} ms | {comps_seq:3d} comparações")

    print("  " + "-" * 50)

    if resultados_hash:
        for filme in resultados_hash:
            exibir_filme(filme)
    else:
        print(" ✕ Nenhum filme encontrado com esse título.")


def inserir(filmes, blocos, indice):
    novo_id = max(f['id'] for f in filmes) + 1
    
    print("\n ╭─ Inserir Novo Filme")
    titulo = input(" ├─ Título........: ").strip()
    ano = int(input(" ├─ Ano...........: "))
    genero = input(" ├─ Gênero........: ").strip()
    pais = input(" ├─ País..........: ").strip()
    nacionalidade = input(" ├─ Nacionalidade.: ").strip()
    distribuidora = input(" ├─ Distribuidora.: ").strip()
    origem = input(" ╰─ Origem........: ").strip()
    
    novo_filme = {
        'id': novo_id,
        'Ano de exibição': ano,
        'Título da obra': titulo,
        'Gênero': genero,
        'País(es) produtor(es) da obra': pais,
        'Nacionalidade da obra': nacionalidade,
        'Empresa distribuidora': distribuidora,
        'Origem da empresa distribuidora': origem
    }
    
    inicio = time.perf_counter()
    filmes.append(novo_filme)
    tempo_lista = (time.perf_counter() - inicio) * 1000
    
    inicio = time.perf_counter()
    inserir_filme(blocos, indice, novo_filme)
    tempo_idx = (time.perf_counter() - inicio) * 1000
    
    print("\n  [ DESEMPENHO DA INSERÇÃO ]")
    print(f"  • Lista....: {tempo_lista:.3f} ms")
    print(f"  • Indexada.: {tempo_idx:.3f} ms")
    print(f"\n  ✓ Sucesso: Filme ID {novo_id} inserido no sistema!")

def excluir(filmes, blocos, indice):
    print("\n [ EXCLUIR FILME ]")
    print(" [ 1 ] 🔢 Por ID")
    print(" [ 2 ] 🔤 Por Nome")
    
    opcao = input("\n  ╰─❯ Selecione a opção: ").strip()
    
    if opcao == "1":
        print("\n  ╭─ Exclusão por ID")
        try:
            id_excluir = int(input("  ╰─❯ Digite o ID: "))
        except ValueError:
            print("\n  [!] Erro: ID inválido!")
            return
        
        inicio = time.perf_counter()
        filme_removido = None
        for i, filme in enumerate(filmes):
            if filme['id'] == id_excluir:
                filme_removido = filmes.pop(i)
                break
        tempo_lista = (time.perf_counter() - inicio) * 1000
        
        if not filme_removido:
            print("\n  [!] Filme não encontrado no sistema!")
            return
        
        inicio = time.perf_counter()
        excluir_filme(blocos, indice, id_excluir)
        tempo_idx = (time.perf_counter() - inicio) * 1000
        
        print("\n  [ DESEMPENHO DA EXCLUSÃO ]")
        print(f"  • Lista....: {tempo_lista:.3f} ms")
        print(f"  • Indexada.: {tempo_idx:.3f} ms")
        print(f"\n  ✓ Sucesso: Filme ID {id_excluir} excluído!")
    
    elif opcao == "2":
        print("\n  ╭─ Exclusão por Título")
        nome = input("  ╰─❯ Digite o Título: ").strip()
        resultados = buscar_por_nome_sequencial(filmes, nome)
        
        if not resultados:
            print("\n [!] Nenhum filme encontrado com esse título!")
            return
        
        print("\n  [ FILMES ENCONTRADOS ]")
        for i, filme in enumerate(resultados):
            print(f"  [{i+1:2d}] {filme['Título da obra']} ({filme['Ano de exibição']}) - ID: {filme['id']}")
        
        print("\n  ╭─ Selecione o filme para exclusão")
        try:
            escolha = int(input("  ╰─❯ Qual excluir? (0 para cancelar): "))
        except ValueError:
            print("\n  [!] Erro: Opção inválida!")
            return
        
        if escolha == 0:
            print("\n  Operação cancelada.")
            return
        
        if escolha < 1 or escolha > len(resultados):
            print("\n  [!] Erro: Opção inválida!")
            return
        
        filme_removido = resultados[escolha - 1]
        
        inicio = time.perf_counter()
        filmes.remove(filme_removido)
        tempo_lista = (time.perf_counter() - inicio) * 1000
        
        inicio = time.perf_counter()
        excluir_filme(blocos, indice, filme_removido['id'])
        tempo_idx = (time.perf_counter() - inicio) * 1000
        
        print("\n  [ DESEMPENHO DA EXCLUSÃO ]")
        print(f"  • Lista....: {tempo_lista:.3f} ms")
        print(f"  • Indexada.: {tempo_idx:.3f} ms")
        print(f"\n  ✓ Sucesso: Filme ID {filme_removido['id']} ('{filme_removido['Título da obra']}') excluído!")

def main():
    caminho_csv = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'filmes.csv'
    )

    filmes = carregar_csv(caminho_csv)
    
    if not filmes:
        print("\n [!] Erro: Nenhum filme carregado!")
        return
    
    blocos, indice = construir_indice(filmes)
    hash_titulos = criar_hash_titulos(filmes)
    
    while True:
        print("\n")
        print(" ╔════════════════════════════════════════╗")
        print(" ║       SISTEMA DE BUSCA DE FILMES       ║")
        print(" ╚════════════════════════════════════════╝")
        print(" [ 1 ] 🔍 Buscar Filme")
        print(" [ 2 ] ➕ Inserir Filme")
        print(" [ 3 ] 🗑️  Excluir Filme")
        print(" [ 0 ] 🚪 Sair do Sistema")
        
        opcao = input("\n ╰─❯ Escolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n [ MÉTODO DE BUSCA ]")
            print(" [ 1 ] 🔢 Por ID")
            print(" [ 2 ] 🔤 Por Nome")
            tipo = input("\n ╰─❯ Selecione: ").strip()
            
            if tipo == "1":
                buscar_por_id(filmes, blocos, indice)
            elif tipo == "2":
                buscar_por_nome(filmes, hash_titulos)
            else:
                print("\n  [!] Opção inválida!")
        
        elif opcao == "2":
            inserir(filmes, blocos, indice)
        
        elif opcao == "3":
            excluir(filmes, blocos, indice)
        
        elif opcao == "0":
            print("\n ╭─ Encerrar o Sistema")
            salvar = input(" ╰─❯ Salvar alterações no CSV? (s/n): ").strip().lower()
            if salvar == "s":
                salvar_csv(caminho_csv, filmes)
                print("      ✓ Alterações salvas com sucesso.")
            print("\n  Saindo... Até logo!\n")
            break
        else:
            print("\n  [!] Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()