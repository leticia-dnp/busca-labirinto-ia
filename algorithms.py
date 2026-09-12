"""
algorithms.py

DISCIPLINA: INTELIGÊNCIA ARTIFICIAL - UFGD
DOCENTE: Alexandre Augusto A. de Souza
DISCENTES: Letícia do Nascimento Pereira e Vagner S. Rocha Junior
TRABALHO - P1 

Implementação dos três algoritmos de busca (BFS, DFS e A*) usados pelo
Maze Solver para encontrar um caminho entre maze.inicio e maze.objetivo.

"""

import time
import heapq
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Tuple

Coord = Tuple[int, int]


@dataclass
class SearchResult:
    encontrado: bool            # True se um caminho até o objetivo foi achado
    caminho: List[Coord]        # sequência de células do início ao objetivo 
    explorados: List[Coord]     # células visitadas, na ordem em que foram exploradas
    expandidos: int             # nós processados
    tempo: float                # tempo de execução em segundos


def reconstruir_caminho(veio_de: Dict[Coord, Coord], inicio: Coord, objetivo: Coord) -> List[Coord]:
    """A partir do dicionário veio_de (onde veio_de[celula] guarda de qual
    célula se chegou até `celula`), reconstrói e devolve a lista de células
    do início até o objetivo, na ordem correta."""
    caminho = [objetivo]
    atual = objetivo
    while atual != inicio:
        atual = veio_de[atual]
        caminho.append(atual)
    caminho.reverse()
    return caminho


def heuristica(a: Coord, b: Coord) -> int:
    """Distância de Manhattan entre duas células (usada como h(n) no A*)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def bfs(maze) -> SearchResult:
    """Busca em Largura (BFS).

    Explora o labirinto "em camadas", sempre processando primeiro as
    células descobertas há mais tempo (estrutura FIFO - fila, via
    collections.deque). Como todas as arestas têm o mesmo custo (um passo),
    a BFS garante encontrar o caminho mais curto em número de células.
    """
    inicio_tempo = time.perf_counter()

    inicio = maze.inicio
    objetivo = maze.objetivo

    fronteira = deque([inicio])
    conhecidos = {inicio}              # evita que a mesma célula seja inserida duas vezes na fronteira
    veio_de: Dict[Coord, Coord] = {}
    explorados: List[Coord] = []

    while fronteira:
        celula = fronteira.popleft()
        explorados.append(celula)

        if celula == objetivo:
            caminho = reconstruir_caminho(veio_de, inicio, objetivo)
            tempo = time.perf_counter() - inicio_tempo
            return SearchResult(
                encontrado=True,
                caminho=caminho,
                explorados=explorados,
                expandidos=len(explorados),
                tempo=tempo,
            )

        for vizinho in maze.vizinhos(celula):
            if vizinho not in conhecidos:
                conhecidos.add(vizinho)
                veio_de[vizinho] = celula
                fronteira.append(vizinho)

    tempo = time.perf_counter() - inicio_tempo
    return SearchResult(
        encontrado=False,
        caminho=[],
        explorados=explorados,
        expandidos=len(explorados),
        tempo=tempo,
    )


def dfs(maze) -> SearchResult:
    """Busca em Profundidade (DFS).

    Segue por um caminho até não poder mais avançar, antes de voltar
    (backtrack) e tentar outro ramo. Usa uma pilha (lista Python com
    append/pop - estrutura LIFO). Diferente da BFS, a DFS não garante o
    caminho mais curto, mas costuma expandir menos células.
    """
    inicio_tempo = time.perf_counter()

    inicio = maze.inicio
    objetivo = maze.objetivo

    fronteira = [inicio]              # pilha (LIFO)
    conhecidos = {inicio}
    veio_de: Dict[Coord, Coord] = {}
    explorados: List[Coord] = []

    while fronteira:
        celula = fronteira.pop()
        explorados.append(celula)

        if celula == objetivo:
            caminho = reconstruir_caminho(veio_de, inicio, objetivo)
            tempo = time.perf_counter() - inicio_tempo
            return SearchResult(
                encontrado=True,
                caminho=caminho,
                explorados=explorados,
                expandidos=len(explorados),
                tempo=tempo,
            )

        for vizinho in maze.vizinhos(celula):
            if vizinho not in conhecidos:
                conhecidos.add(vizinho)
                veio_de[vizinho] = celula
                fronteira.append(vizinho)

    tempo = time.perf_counter() - inicio_tempo
    return SearchResult(
        encontrado=False,
        caminho=[],
        explorados=explorados,
        expandidos=len(explorados),
        tempo=tempo,
    )


def astar(maze) -> SearchResult:
    """Busca A* (A-estrela).

    Combina o custo já percorrido g(n) com uma estimativa do custo restante
    h(n) = heuristica(n, maze.objetivo), expandindo sempre a célula de
    menor f(n) = g(n) + h(n). Usa uma fila de prioridade (heapq), inserindo
    tuplas (f, contador, celula) - o contador evita comparar células
    diretamente em caso de empate de f.

    Observação de implementação: diferente de BFS/DFS (onde cada célula só
    pode ser inserida uma única vez na fronteira, pois qualquer caminho até
    ela tem o mesmo custo), no A* o custo g(n) pode ser melhorado depois que
    uma célula já foi descoberta por outro caminho. Por isso guardamos o
    melhor g conhecido para cada célula e permitimos "relaxar" (atualizar)
    esse valor quando um caminho mais barato é encontrado, reinserindo a
    célula na fila de prioridade. Um conjunto de "fechados" garante que cada
    célula só seja efetivamente expandida (processada/contabilizada em
    `explorados`) uma única vez, com seu menor custo já garantido - isso é o
    que assegura que a BFS e o A* encontrem sempre o caminho mais curto.
    """
    inicio_tempo = time.perf_counter()

    inicio = maze.inicio
    objetivo = maze.objetivo

    contador = 0
    fronteira = [(heuristica(inicio, objetivo), contador, inicio)]
    custo_g: Dict[Coord, int] = {inicio: 0}
    veio_de: Dict[Coord, Coord] = {}
    fechados = set()
    explorados: List[Coord] = []

    while fronteira:
        _, _, celula = heapq.heappop(fronteira)

        if celula in fechados:
            continue
        fechados.add(celula)
        explorados.append(celula)

        if celula == objetivo:
            caminho = reconstruir_caminho(veio_de, inicio, objetivo)
            tempo = time.perf_counter() - inicio_tempo
            return SearchResult(
                encontrado=True,
                caminho=caminho,
                explorados=explorados,
                expandidos=len(explorados),
                tempo=tempo,
            )

        for vizinho in maze.vizinhos(celula):
            novo_g = custo_g[celula] + 1
            if vizinho not in custo_g or novo_g < custo_g[vizinho]:
                custo_g[vizinho] = novo_g
                veio_de[vizinho] = celula
                f = novo_g + heuristica(vizinho, objetivo)
                contador += 1
                heapq.heappush(fronteira, (f, contador, vizinho))

    tempo = time.perf_counter() - inicio_tempo
    return SearchResult(
        encontrado=False,
        caminho=[],
        explorados=explorados,
        expandidos=len(explorados),
        tempo=tempo,
    )