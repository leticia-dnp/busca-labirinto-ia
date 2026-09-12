"""
ui.py
Componentes visuais reutilizáveis: cores da paleta, classes Botao e
Dropdown, a função desenhar_tabuleiro (pinta cada célula do labirinto de
acordo com as listas de exploradas/caminho) e desenhar_legenda.

Arquivo já pronto - NAO deve ser alterado para a implementacao basica.
"""

import pygame

# --- Layout ---
TAMANHO_CELULA = 28
MARGEM_TOPO = 60
MARGEM_LATERAL = 20
ALTURA_RODAPE = 70

# --- Paleta de cores ---
COR_FUNDO = (30, 33, 41)
COR_TABULEIRO = (45, 49, 61)
COR_PAREDE = (18, 18, 22)
COR_INICIO = (46, 204, 113)
COR_OBJETIVO = (231, 76, 155)
COR_EXPLORADO = (93, 156, 236)
COR_CAMINHO = (245, 197, 107)
COR_TEXTO = (230, 230, 235)
COR_BOTAO = (52, 168, 83)
COR_BOTAO2 = (66, 133, 244)
COR_BOTAO_TEXTO = (255, 255, 255)
COR_DROPDOWN = (60, 64, 78)


class Botao:
    def __init__(self, x, y, largura, altura, texto, cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor

    def desenhar(self, tela, fonte):
        pygame.draw.rect(tela, self.cor, self.rect, border_radius=6)
        texto_surf = fonte.render(self.texto, True, COR_BOTAO_TEXTO)
        tela.blit(texto_surf, texto_surf.get_rect(center=self.rect.center))

    def clicado(self, pos):
        return self.rect.collidepoint(pos)


class Dropdown:
    def __init__(self, x, y, largura, altura, opcoes):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.opcoes = opcoes
        self.selecionado = 0
        self.aberto = False

    def desenhar(self, tela, fonte):
        pygame.draw.rect(tela, COR_DROPDOWN, self.rect, border_radius=6)
        texto_surf = fonte.render(self.opcoes[self.selecionado], True, COR_TEXTO)
        tela.blit(texto_surf, (self.rect.x + 10, self.rect.y + (self.rect.height - texto_surf.get_height()) // 2))
        if self.aberto:
            for i, opcao in enumerate(self.opcoes):
                r = pygame.Rect(self.rect.x, self.rect.y + self.rect.height * (i + 1), self.rect.width, self.rect.height)
                pygame.draw.rect(tela, COR_DROPDOWN, r, border_radius=6)
                t = fonte.render(opcao, True, COR_TEXTO)
                tela.blit(t, (r.x + 10, r.y + (r.height - t.get_height()) // 2))

    def clique(self, pos):
        if self.rect.collidepoint(pos):
            self.aberto = not self.aberto
            return True
        if self.aberto:
            for i in range(len(self.opcoes)):
                r = pygame.Rect(self.rect.x, self.rect.y + self.rect.height * (i + 1), self.rect.width, self.rect.height)
                if r.collidepoint(pos):
                    self.selecionado = i
                    self.aberto = False
                    return True
            self.aberto = False
        return False

    def valor(self):
        return self.opcoes[self.selecionado]


def desenhar_tabuleiro(tela, maze, explorados=None, caminho=None):
    """Pinta cada célula do labirinto conforme seu papel na busca."""
    explorados = explorados or []
    caminho = caminho or []
    caminho_set = set(caminho)
    explorados_set = set(explorados)

    for linha in range(maze.linhas):
        for coluna in range(maze.colunas):
            celula = (linha, coluna)
            x = MARGEM_LATERAL + coluna * TAMANHO_CELULA
            y = MARGEM_TOPO + linha * TAMANHO_CELULA
            rect = pygame.Rect(x, y, TAMANHO_CELULA - 2, TAMANHO_CELULA - 2)

            if not maze.eh_livre(celula):
                cor = COR_PAREDE
            elif celula == maze.inicio:
                cor = COR_INICIO
            elif celula == maze.objetivo:
                cor = COR_CAMINHO if celula in caminho_set else COR_OBJETIVO
            elif celula in caminho_set:
                cor = COR_CAMINHO
            elif celula in explorados_set:
                cor = COR_EXPLORADO
            else:
                cor = COR_TABULEIRO

            pygame.draw.rect(tela, cor, rect, border_radius=3)


def desenhar_legenda(tela, fonte, y):
    itens = [
        (COR_INICIO, "Início"),
        (COR_OBJETIVO, "Objetivo"),
        (COR_PAREDE, "Parede"),
        (COR_EXPLORADO, "Explorado"),
        (COR_CAMINHO, "Caminho"),
    ]
    x = MARGEM_LATERAL
    for cor, nome in itens:
        pygame.draw.rect(tela, cor, pygame.Rect(x, y, 14, 14), border_radius=3)
        t = fonte.render(nome, True, COR_TEXTO)
        tela.blit(t, (x + 20, y - 2))
        x += 20 + t.get_width() + 20
