"""
maze.py
Define a classe Maze (grade do labirinto, início, objetivo e métodos de
consulta) e a função gerar_labirinto, que cria labirintos aleatórios
garantidamente solúveis.

Arquivo já pronto - NAO deve ser alterado para a implementacao basica.
"""

import random

Coord = tuple  # (linha, coluna)


class Maze:
    """Representa o labirinto como uma grade (matriz) de células livres e paredes."""

    def __init__(self, grid, inicio, objetivo):
        self.grid = grid  # grid[linha][coluna] -> True (livre) / False (parede)
        self.linhas = len(grid)
        self.colunas = len(grid[0]) if self.linhas > 0 else 0
        self.inicio = inicio
        self.objetivo = objetivo

    def eh_valida(self, celula):
        """Verifica se a célula está dentro dos limites do tabuleiro."""
        linha, coluna = celula
        return 0 <= linha < self.linhas and 0 <= coluna < self.colunas

    def eh_livre(self, celula):
        """Verifica se a célula existe e não é parede."""
        if not self.eh_valida(celula):
            return False
        linha, coluna = celula
        return self.grid[linha][coluna]

    def vizinhos(self, celula):
        """Devolve a lista de células vizinhas válidas e livres (cima, baixo,
        esquerda, direita) de `celula`."""
        linha, coluna = celula
        candidatos = [
            (linha - 1, coluna),   # cima
            (linha + 1, coluna),   # baixo
            (linha, coluna - 1),   # esquerda
            (linha, coluna + 1),   # direita
        ]
        return [c for c in candidatos if self.eh_livre(c)]


def _alcancaveis(grid, origem):
    """BFS auxiliar usada apenas na geração, para garantir que o labirinto
    tenha solução entre início e objetivo."""
    linhas = len(grid)
    colunas = len(grid[0])
    visitados = {origem}
    fila = [origem]
    idx = 0
    while idx < len(fila):
        linha, coluna = fila[idx]
        idx += 1
        for dl, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            viz = (linha + dl, coluna + dc)
            vl, vc = viz
            if 0 <= vl < linhas and 0 <= vc < colunas and grid[vl][vc] and viz not in visitados:
                visitados.add(viz)
                fila.append(viz)
    return visitados


def gerar_labirinto(linhas=15, colunas=20, prob_parede=0.28, seed=None):
    """Gera um labirinto aleatório (linhas x colunas), com início no canto
    superior esquerdo e objetivo no canto inferior direito, garantidamente
    solúvel."""
    rng = random.Random(seed)
    while True:
        grid = [[rng.random() > prob_parede for _ in range(colunas)] for _ in range(linhas)]
        inicio = (0, 0)
        objetivo = (linhas - 1, colunas - 1)
        grid[inicio[0]][inicio[1]] = True
        grid[objetivo[0]][objetivo[1]] = True
        if objetivo in _alcancaveis(grid, inicio):
            return Maze(grid, inicio, objetivo)
