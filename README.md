# G15_Busca_EDA2-2026.2
Trabalho 1 da disciplina Estrutura de Dados 2, semestre 2026.2.

## Sistema de Busca de Filmes

Este projeto foi desenvolvido para o Trabalho 1 de **Estrutura de Dados 2**, com o objetivo de implementar e comparar, na prática, diferentes algoritmos de busca sobre uma base de dados real.

O sistema permite **buscar, inserir e excluir filmes** de uma base com mais de 7 mil registros, utilizando três estruturas de busca diferentes:

1. **Busca sequencial** — percorre a lista item a item (busca por ID e por Título);
2. **Busca sequencial indexada** — divide os dados em blocos e usa um índice para pular direto ao bloco correto (busca por ID);
3. **Busca por hashing** — usa uma **tabela hash construída do zero** (função hash própria, colisão por encadeamento separado, redimensionamento dinâmico) para localizar filmes por título em tempo praticamente constante.

A cada busca, o programa mede e exibe o **tempo de execução (ms)** e o **número de comparações/operações** de cada método, permitindo visualizar na prática a diferença de desempenho entre eles, o mesmo raciocínio por trás das complexidades O(n), O(√n) e O(1) estudadas em sala.

## Fonte dos dados

A base de dados é composta por informações sobre **filmes brasileiros e estrangeiros exibidos no Brasil entre 2009 e 2019**, obtida em formato `.csv` através do Kaggle:

**[Análise dos Filmes Exibidos (2009–2019) — Kaggle](https://www.kaggle.com/datasets/pedrothiago/anlise-dos-filmes-exibidos-2009-a-2019)**

O arquivo já vem com os dados tratados e está disponível diretamente no repositório em [`filmes.csv`](./filmes.csv), com **7.052 registros** e as seguintes colunas:

| Coluna | Descrição |
|---|---|
| `id` | Identificador único do filme (gerado ao carregar o CSV) |
| `Ano de exibição` | Ano em que o filme foi exibido |
| `Título da obra` | Nome do filme |
| `Gênero` | Gênero da obra |
| `País(es) produtor(es) da obra` | País(es) de produção |
| `Nacionalidade da obra` | Nacional ou Estrangeira |
| `Empresa distribuidora` | Distribuidora responsável |
| `Origem da empresa distribuidora` | Origem da distribuidora |
| `Público no ano de exibição` | Público total no ano |
| `Renda (R$) no ano de exibição` | Renda gerada no ano |

## Estrutura do repositório

```
G15_Busca_EDA2-2026.2/
├── filmes.csv                  # base de dados (7.052 filmes)
├── README.md                   # este arquivo
├── src/
│   ├── main.py                 # ponto de entrada (menu em modo texto)
│   ├── gui.py                  # interface gráfica (Tkinter)
│   ├── leitura_csv.py          # leitura/escrita do CSV + normalização de título
│   ├── busca_sequencial.py     # busca sequencial (por ID e por Título)
│   ├── busca_indexada.py       # busca sequencial indexada (por ID)
│   └── busca_hash.py           # tabela hash própria (por Título)
└── tests/
    └── teste_desempenho.py     # gera os números da tabela de desempenho abaixo
```

## Como executar

Pré-requisito: **Python 3** (nenhuma biblioteca externa é necessária — tudo usa apenas a biblioteca padrão).

Modo texto (menu no terminal):

```bash
python3 src/main.py
ou
python -m src.main
```

Interface gráfica (janela com abas Buscar / Inserir / Excluir, com autocomplete no campo de título):

```bash
python3 src/gui.py
ou
python -m src.gui
```

> A interface gráfica usa `tkinter`, que já vem com o Python na maioria dos sistemas. Se aparecer `ModuleNotFoundError: No module named 'tkinter'` no Linux, instale com `sudo apt install python3-tk`.

Ambos os modos leem e gravam no mesmo `filmes.csv`, na raiz do projeto.

## Algoritmos implementados

### 1. Busca Sequencial (`busca_sequencial.py`)
Percorre a lista de filmes do início ao fim comparando cada elemento com a chave buscada. Implementada tanto para busca por **ID** quanto por **Título** (com normalização de acentos/caixa via `normalizar_titulo`, para que a comparação seja justa com a busca por hash).

### 2. Busca Sequencial Indexada (`busca_indexada.py`)
Divide a lista (ordenada por ID) em **blocos de tamanho √n**, e mantém um índice com o primeiro ID de cada bloco. Na busca, primeiro localiza o bloco correto pelo índice, depois percorre **apenas os elementos daquele bloco**. Suporta inserção (no último bloco, com redistribuição quando ele enche) e exclusão (com compactação do bloco).

### 3. Busca por Hashing (`busca_hash.py`)
Tabela hash **implementada do zero** (sem `dict`, `set` ou `hash()` do Python):
- **Função hash própria**, no estilo *djb2*, que transforma o título normalizado em um índice de balde;
- **Colisão por encadeamento separado**: cada balde é uma lista de pares `[chave, filmes]`;
- **Redimensionamento automático**: quando o fator de carga passa de `0.7`, a tabela dobra de capacidade (sempre para um número primo) e todas as chaves são reespalhadas, mantendo o tempo médio O(1).

## Complexidade e resultados de desempenho

### Complexidade teórica

| Algoritmo | Chave | Estrutura | Melhor caso | Pior caso |
|---|---|---|:---:|:---:|
| Busca Sequencial | ID | Lista (ordem do CSV) | O(1) | O(n) |
| Busca Sequencial Indexada | ID | Blocos de √n + índice | O(1) | O(√n) |
| Busca Sequencial | Título | Lista (ordem do CSV) | O(n)¹ | O(n) |
| Busca por Hashing | Título | Tabela hash própria (encadeamento) | O(1) | O(k)² |

¹ A busca sequencial por título **não para no primeiro resultado**, ela precisa varrer a lista inteira mesmo assim, porque pode haver mais de um filme com o mesmo título (retorna todos). Por isso, ao contrário da busca por ID, aqui o melhor e o pior caso coincidem: é sempre O(n).
² *k* é o tamanho do maior balde da tabela (na prática, muito menor que n — ver medição abaixo).

### Resultados medidos (base real, 7.052 filmes)

Medições feitas com `time.perf_counter()`, tirando a média de várias repetições para reduzir ruído (a mesma métrica que o programa mostra ao usuário em cada busca).

**Busca por ID:**

| Método | Caso | Tempo médio | Comparações |
|---|---|---:|---:|
| Sequencial | Melhor (1º elemento) | 0,00012 ms | 1 |
| Sequencial | Pior (inexistente/último) | 0,285 ms | 7.052 |
| Sequencial | Médio (60 amostras aleatórias) | 0,108 ms | 3.008 |
| Indexada | Melhor (1º bloco) | 0,00033 ms | 3 |
| Indexada | Pior (último bloco) | 0,0056 ms | 168 |
| Indexada | Médio (60 amostras aleatórias) | 0,0029 ms | 82 |

**Busca por Título** (base com 4.854 títulos únicos; blocos de √7052 ≈ 83 itens, 85 blocos ao todo; tabela hash com capacidade final 6.947 e fator de carga 0,699):

| Método | Caso | Tempo médio | Comparações/Operações |
|---|---|---:|---:|
| Sequencial | Sempre (ver nota¹) | ≈ 16,3 ms | 7.052 |
| Hash | Melhor (balde sem colisão) | 0,0056 ms | 2 |
| Hash | Pior real (maior balde, 6 itens) | 0,0033 ms | 7 |
| Hash | Médio (40 amostras aleatórias) | 0,0055 ms | 2,15 |

**Principais observações:**
- Na busca por **ID**, a indexada é, em média, cerca de **37× mais rápida** que a sequencial, e no pior caso a diferença é ainda maior (168 comparações contra 7.052).
- Na busca por **Título**, a diferença é a mais dramática do projeto: a busca por hash é, em média, cerca de **3.000× mais rápida** que a sequencial (a sequencial sempre varre os 7.052 registros; a hash resolve com 2 a 3 operações na maioria dos casos).
- O maior balde da tabela hash tem apenas **6 itens colidindo** entre 4.854 chaves distintas, provando que a função hash própria (djb2) e o redimensionamento automático estão distribuindo bem as chaves.
- Em uma escala de microssegundos, o tempo em ms sofre ruído de medição do próprio interpretador Python; por isso, o **número de comparações/operações** é a métrica mais confiável para comparar os algoritmos entre si e os tempos servem para ilustrar a ordem de grandeza real da diferença.

## 🧪 Como reproduzir os testes de desempenho
 
Os números da tabela acima **não são estimados** — foram gerados pelo script [`tests/teste_desempenho.py`](./tests/teste_desempenho.py), rodando direto sobre o `filmes.csv` real (7.052 filmes). Para reproduzir partindo da raiz:
 
```bash
python -m tests.teste_desempenho
```
 
**Como o script mede cada caso:**
 
- **Repetição + média**: uma busca isolada dura microssegundos, tempo curto demais pra confiar num único cronômetro. Por isso cada busca é repetida várias vezes seguidas (500× para as mais rápidas, menos para a sequencial por título, que já é lenta sozinha) e o script divide o tempo total pelo número de repetições.
- **Melhor caso**: usa uma chave escolhida para dar o resultado mais rápido possível, por exemplo, o primeiro elemento da lista para a busca por ID.
- **Pior caso**: usa uma chave que força o máximo de trabalho, um ID inexistente (obriga a varrer tudo), ou, no caso da hash, a **última chave do maior balde real da tabela** (o script primeiro localiza esse balde na estrutura de dados, não chuta um valor).
- **Caso médio**: tira uma amostra aleatória de IDs/títulos reais da base (`random.seed(7)`, fixa) e mede a média do tempo e das comparações sobre essa amostra — a mesma seed garante que a amostra é sempre a mesma entre execuções, então o resultado é reprodutível (o tempo em ms pode variar um pouco conforme a máquina, mas o número de comparações/operações deve se manter igual).
 
## Interface gráfica

Além do menu em modo texto, o projeto conta com uma interface gráfica simples (`src/gui.py`, Tkinter) com três abas:

- **🔍 Buscar** — por ID ou por Título, com autocomplete de títulos e comparação de desempenho entre os métodos lado a lado;
- **➕ Inserir** — formulário para adicionar um novo filme;
- **🗑️ Excluir** — busca por ID ou título e remove o filme selecionado.

## 📸 Capturas de tela

> Adicione as imagens em `docs/screenshots/` e ajuste os caminhos abaixo.

| Menu principal (modo texto) | Interface gráfica — Buscar |
|---|---|
| ![Menu principal](docs/screenshots/menu-principal.png) | ![Aba Buscar](docs/screenshots/gui-buscar.png) |

| Resultado de uma busca por título | Interface gráfica — Inserir |
|---|---|
| ![Resultado da busca](docs/screenshots/resultado-busca.png) | ![Aba Inserir](docs/screenshots/gui-inserir.png) |

## Vídeo de apresentação

 **Link do vídeo:** *[adicionar link do YouTube/Drive aqui]*

## Equipe

<div align="center">

| [<img src="https://res.cloudinary.com/dll5ypaj7/image/fetch/f_auto,w_250,h_250,c_fill,r_30,bo_2px_solid_rgb:2d333b/https://github.com/eduarda-ogomes.png" width="200">](https://github.com/eduarda-ogomes)<br><nobr><sub style="font-size: 160%;">Maria Eduarda de Oliveira</sub></nobr> | [<img src="https://res.cloudinary.com/dll5ypaj7/image/fetch/f_auto,w_250,h_250,c_fill,r_30,bo_2px_solid_rgb:2d333b/https://github.com/pwdrinho.png" width="200">](https://github.com/pwdrinho)<br><nobr><sub style="font-size: 160%;">Pedro Lucas Barbosa</sub></nobr> |
| :---: | :---: |
| 21/1030658 | 241025710 |

</div>

---

## Referências

- Base de dados: [Análise dos Filmes Exibidos (2009–2019) — Kaggle](https://www.kaggle.com/datasets/pedrothiago/anlise-dos-filmes-exibidos-2009-a-2019)