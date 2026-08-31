# ============================================================
# ARQUIVO: src/busca_hash.py
#
# DESCRIÇÃO:
#   - Implementa a busca por hashing usando uma TABELA HASH
#     construída do zero (sem usar dict, set ou hash() do Python).
#
# ESTRUTURA (classe TabelaHash):
#   - Vetor de "baldes" (lista de listas) -> tratamento de colisão
#     por ENCADEAMENTO SEPARADO (separate chaining).
#   - Cada balde guarda pares [chave, lista_de_filmes].
#   - Função hash própria (estilo djb2): percorre os caracteres
#     do título normalizado e vai acumulando um valor numérico,
#     depois reduz pelo tamanho do vetor (módulo) para achar o
#     índice do balde.
#   - Fator de carga (elementos / capacidade) é monitorado; quando
#     ultrapassa 0.7, a tabela é redimensionada (dobra de tamanho
#     e todas as chaves são reespalhadas) para manter O(1) médio.
#
# FUNÇÕES EXPOSTAS (mantêm a mesma assinatura de antes, para não
# precisar mudar o main.py):
#   - criar_hash_titulos(filmes): monta a TabelaHash com os filmes.
#   - buscar_por_hash_titulos(hash_titulos, nome_busca): busca.
#   - buscar_por_hash_titulos_operacoes(hash_titulos, nome_busca):
#       busca contando operações (comparações feitas dentro do
#       balde, já que a colisão é resolvida percorrendo uma lista).
#
# COMPLEXIDADE:
#   - Tempo médio: O(1) por operação (hash bem distribuída e fator
#     de carga controlado).
#   - Pior caso: O(n) se todas as chaves colidirem no mesmo balde
#     (na prática não acontece, pois a função hash espalha bem e
#     o redimensionamento evita baldes muito cheios).
#   - Espaço: O(n) para armazenar os baldes.
#
# OBSERVAÇÕES:
#   - Diferente da versão anterior (dict do Python), aqui TODA a
#     lógica de hashing, colisão e redimensionamento é nossa.
#   - normalizar_titulo() continua vindo de leitura_csv.py, pois
#     é usada tanto pela busca sequencial quanto pela por hash,
#     garantindo que as duas retornem o mesmo conjunto de resultados.
# ============================================================

from leitura_csv import normalizar_titulo


class TabelaHash:
    """
    Tabela hash própria, com colisão resolvida por encadeamento
    separado (cada balde é uma lista de pares [chave, valor]).
    """

    # Fator de carga máximo tolerado antes de redimensionar.
    FATOR_DE_CARGA_MAXIMO = 0.7

    def __init__(self, capacidade_inicial=101):
        # capacidade_inicial já nasce como número primo para reduzir
        # o agrupamento de chaves em poucos baldes (menos colisões).
        self.capacidade = self._proximo_primo(capacidade_inicial)
        self.baldes = [[] for _ in range(self.capacidade)]
        self.quantidade_chaves = 0  # nº de chaves distintas armazenadas

    # --------------------------------------------------------
    # FUNÇÃO HASH (própria, estilo djb2)
    # --------------------------------------------------------
    def _funcao_hash(self, chave):
        """
        Transforma uma string (título normalizado) em um índice
        dentro do vetor de baldes.

        Ideia do djb2: começa com um valor "semente" (5381) e, para
        cada caractere, multiplica o acumulado por 33 e soma o
        código do caractere (ord). A multiplicação por 33 ajuda a
        espalhar bem os valores mesmo para strings parecidas.
        """
        valor_hash = 5381

        for caractere in chave:
            valor_hash = (valor_hash * 33 + ord(caractere)) & 0xFFFFFFFF

        return valor_hash % self.capacidade

    # --------------------------------------------------------
    # PRIMOS (para escolher bons tamanhos de tabela)
    # --------------------------------------------------------
    def _eh_primo(self, n):
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False

        divisor = 3
        while divisor * divisor <= n:
            if n % divisor == 0:
                return False
            divisor += 2

        return True

    def _proximo_primo(self, n):
        candidato = max(n, 2)
        while not self._eh_primo(candidato):
            candidato += 1
        return candidato

    # --------------------------------------------------------
    # FATOR DE CARGA E REDIMENSIONAMENTO
    # --------------------------------------------------------
    def _fator_de_carga(self):
        return self.quantidade_chaves / self.capacidade

    def _redimensionar(self):
        """
        Dobra (aproximadamente) a capacidade da tabela e reinsere
        todas as chaves já existentes, recalculando o índice de
        cada uma com a nova capacidade (rehash).
        """
        baldes_antigos = self.baldes

        self.capacidade = self._proximo_primo(self.capacidade * 2)
        self.baldes = [[] for _ in range(self.capacidade)]
        self.quantidade_chaves = 0

        for balde in baldes_antigos:
            for chave, lista_filmes in balde:
                self._inserir_bruto(chave, lista_filmes)

    def _inserir_bruto(self, chave, lista_filmes):
        """Reinsere um par [chave, lista_filmes] sem checar duplicata
        (usado só durante o redimensionamento, onde as chaves já são
        garantidamente únicas)."""
        indice = self._funcao_hash(chave)
        self.baldes[indice].append([chave, lista_filmes])
        self.quantidade_chaves += 1

    # --------------------------------------------------------
    # OPERAÇÕES PÚBLICAS
    # --------------------------------------------------------
    def inserir(self, chave, filme):
        """
        Insere um filme na tabela. Se a chave (título normalizado)
        já existir, o filme é adicionado à lista daquela chave
        (trata duplicatas de título). Se não existir, cria uma
        nova entrada.
        """
        indice = self._funcao_hash(chave)
        balde = self.baldes[indice]

        for par in balde:
            if par[0] == chave:
                par[1].append(filme)
                return

        balde.append([chave, [filme]])
        self.quantidade_chaves += 1

        if self._fator_de_carga() > self.FATOR_DE_CARGA_MAXIMO:
            self._redimensionar()

    def buscar(self, chave):
        """Retorna a lista de filmes associados à chave, ou [] se
        não houver nenhum."""
        indice = self._funcao_hash(chave)
        balde = self.baldes[indice]

        for par in balde:
            if par[0] == chave:
                return par[1]

        return []

    def buscar_com_operacoes(self, chave):
        """
        Igual a buscar(), mas também retorna quantas "operações"
        foram feitas: 1 pelo cálculo do hash/acesso ao balde, mais
        uma para cada comparação de chave dentro do balde (é aí que
        aparecem as colisões, quando o balde tem mais de um par).
        """
        indice = self._funcao_hash(chave)
        balde = self.baldes[indice]

        operacoes = 1  # cálculo do hash + acesso ao balde correspondente

        for par in balde:
            operacoes += 1
            if par[0] == chave:
                return par[1], operacoes

        return [], operacoes


def criar_hash_titulos(filmes):
    """
    Cria a tabela hash dos filmes.

    Chave:
        título normalizado

    Valor:
        lista de filmes com aquele título
    """
    hash_titulos = TabelaHash(capacidade_inicial=101)

    for filme in filmes:
        titulo = filme['Título da obra']
        chave = normalizar_titulo(titulo)
        hash_titulos.inserir(chave, filme)

    return hash_titulos


def buscar_por_hash_titulos(hash_titulos, nome_busca):
    """
    Busca filmes pelo título utilizando a tabela hash.

    Retorna:
        lista de filmes encontrados
    """
    chave = normalizar_titulo(nome_busca)
    return hash_titulos.buscar(chave)


def buscar_por_hash_titulos_operacoes(hash_titulos, nome_busca):
    """
    Busca filmes pelo título utilizando a tabela hash
    e contabiliza a operação de consulta.

    Diferente da busca sequencial/indexada, aqui a maior parte do
    trabalho é O(1): calcular o hash e acessar o balde direto.
    As "operações" contadas são: 1 pelo acesso ao balde + 1 para
    cada comparação de chave feita dentro do balde (o que só cresce
    se houver colisão de hash entre títulos diferentes).

    Retorna:
        resultados: lista de filmes encontrados
        operacoes: quantidade de operações contabilizadas
    """
    chave = normalizar_titulo(nome_busca)
    return hash_titulos.buscar_com_operacoes(chave)