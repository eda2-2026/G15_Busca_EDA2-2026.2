import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from leitura_csv import carregar_csv
from busca_indexada import (
    construir_indice,
    buscar_por_id,
    buscar_por_id_comparacoes,
    inserir_filme,
    excluir_filme,
    redistribuir
)


def exibir_estatisticas(blocos, indice):
    total_filmes = sum(sum(1 for f in bloco if f is not None) for bloco in blocos)
    total_vazios = sum(sum(1 for f in bloco if f is None) for bloco in blocos)
    
    print(f"  Blocos: {len(blocos)}")
    print(f"  Filmes: {total_filmes}")
    print(f"  Vazios: {total_vazios}")
    print(f"  Entradas no índice: {len(indice)}")


def testar_construcao(blocos, indice):
    print("\n[TESTE DE CONSTRUÇÃO]")
    exibir_estatisticas(blocos, indice)
    
    print(f"  Tamanho do bloco: {len(blocos[0])}")
    print(f"  Último bloco: {len(blocos[-1])} posições")
    
    if blocos[-1][-1] is None:
        print(f"  Último bloco tem espaços vazios: ✅")
    else:
        print(f"  Último bloco SEM espaços vazios: ❌")


def testar_busca(blocos, indice):
    print("\n[TESTE DE BUSCA]")
    
    ids_teste = [0, 1, 50, 51, 100, 1000, 5000, 7080]
    
    for id_busca in ids_teste:
        filme, comps = buscar_por_id_comparacoes(blocos, indice, id_busca)
        
        if filme:
            print(f"  ID {id_busca:4d}: {filme['Título da obra'][:40]} ({comps} comparações)")
        else:
            print(f"  ID {id_busca:4d}: NÃO ENCONTRADO ({comps} comparações)")


def testar_busca_inexistente(blocos, indice):
    print("\n[TESTE DE BUSCA - IDs INEXISTENTES]")
    
    for id_busca in [81, 125, 9999]:
        filme, comps = buscar_por_id_comparacoes(blocos, indice, id_busca)
        
        if filme:
            print(f"  ID {id_busca}: ENCONTRADO (deveria ser None)")
        else:
            print(f"  ID {id_busca}: não encontrado ({comps} comparações)")


def testar_insercao(blocos, indice):
    print("\n[TESTE DE INSERÇÃO]")
    
    filme_novo = {
        'id': 9999,
        'Ano de exibição': 2024,
        'Título da obra': 'Filme Teste Indexada',
        'Gênero': 'Ficção',
        'País(es) produtor(es) da obra': 'Brasil',
        'Nacionalidade da obra': 'Brasileira',
        'Empresa distribuidora': 'Teste',
        'Origem da empresa distribuidora': 'Nacional'
    }
    
    resultado = inserir_filme(blocos, indice, filme_novo)
    print(f"  Inserção ID 9999: {resultado}")
    
    filme = buscar_por_id(blocos, indice, 9999)
    if filme:
        print(f"  Busca ID 9999: {filme['Título da obra']}")
    else:
        print(f"  Busca ID 9999: NÃO ENCONTRADO")


def testar_insercao_duplicada(blocos, indice):
    print("\n[TESTE DE INSERÇÃO - DUPLICADA]")
    
    filme_duplicado = {
        'id': 50,
        'Ano de exibição': 2024,
        'Título da obra': 'Filme Duplicado',
        'Gênero': 'Ficção',
        'País(es) produtor(es) da obra': 'Brasil',
        'Nacionalidade da obra': 'Brasileira',
        'Empresa distribuidora': 'Teste',
        'Origem da empresa distribuidora': 'Nacional'
    }
    
    resultado = inserir_filme(blocos, indice, filme_duplicado)
    print(f"  Inserção ID 50 (já existe): {resultado}")
    
    if resultado:
        print(f"  ❌ DEVERIA TER REJEITADO!")
    else:
        print(f"  ✅ Rejeitado corretamente!")


def testar_exclusao(blocos, indice):
    print("\n[TESTE DE EXCLUSÃO]")
    
    resultado = excluir_filme(blocos, indice, 50)
    print(f"  Exclusão ID 50: {resultado}")
    
    filme = buscar_por_id(blocos, indice, 50)
    if filme:
        print(f"  Busca ID 50: AINDA EXISTE ❌")
    else:
        print(f"  Busca ID 50: removido ✅")


def testar_exclusao_inexistente(blocos, indice):
    print("\n[TESTE DE EXCLUSÃO - ID INEXISTENTE]")
    
    resultado = excluir_filme(blocos, indice, 99999)
    print(f"  Exclusão ID 99999: {resultado}")
    
    if resultado:
        print(f"  ❌ DEVERIA RETORNAR False!")
    else:
        print(f"  ✅ Retornou False corretamente!")


if __name__ == "__main__":
    print("=" * 60)
    print("  TESTE DA BUSCA INDEXADA")
    print("=" * 60)
    
    caminho_csv = os.path.join(os.path.dirname(__file__), '..', 'filmes.csv')
    
    filmes = carregar_csv(caminho_csv)
    blocos, indice = construir_indice(filmes)
    
    testar_construcao(blocos, indice)
    testar_busca(blocos, indice)
    testar_busca_inexistente(blocos, indice)
    testar_insercao(blocos, indice)
    testar_insercao_duplicada(blocos, indice)
    testar_exclusao(blocos, indice)
    testar_exclusao_inexistente(blocos, indice)
    
    print("\n[ESTATÍSTICAS FINAIS]")
    exibir_estatisticas(blocos, indice)