"""
main.py
Ponto de entrada da aplicação. Cria a janela pygame, monta a caixa de
seleção e os botões, mantém o loop principal (captura de eventos, animação
e desenho a cada quadro) e chama a função do algoritmo escolhido quando o
botão "Executar" é clicado.

Arquivo já pronto - NAO deve ser alterado para a implementacao basica.
"""

import sys
import pygame

from maze import gerar_labirinto
from ui import (
    Botao,
    Dropdown,
    desenhar_tabuleiro,
    desenhar_legenda,
    TAMANHO_CELULA,
    MARGEM_TOPO,
    MARGEM_LATERAL,
    ALTURA_RODAPE,
    COR_FUNDO,
    COR_TEXTO,
    COR_BOTAO,
    COR_BOTAO2,
)
from algorithms import bfs, dfs, astar

ALGORITMOS = {"BFS": bfs, "DFS": dfs, "A*": astar}

LINHAS = 15
COLUNAS = 20


def main():
    pygame.init()
    largura = MARGEM_LATERAL * 2 + COLUNAS * TAMANHO_CELULA
    altura = MARGEM_TOPO + LINHAS * TAMANHO_CELULA + ALTURA_RODAPE
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Maze Solver — Comparação de Algoritmos de Busca")
    fonte = pygame.font.SysFont("arial", 16)
    fonte_pequena = pygame.font.SysFont("arial", 14)
    relogio = pygame.time.Clock()

    maze = gerar_labirinto(LINHAS, COLUNAS)

    dropdown = Dropdown(100, 15, 100, 30, list(ALGORITMOS.keys()))
    botao_executar = Botao(220, 15, 100, 30, "Executar", COR_BOTAO)
    botao_novo = Botao(330, 15, 130, 30, "Novo Labirinto", COR_BOTAO2)

    resultado = None
    explorados_visiveis = []
    animando = False
    indice_animacao = 0

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos = evento.pos
                if dropdown.clique(pos):
                    pass
                elif botao_executar.clicado(pos):
                    nome = dropdown.valor()
                    resultado = ALGORITMOS[nome](maze)
                    explorados_visiveis = []
                    indice_animacao = 0
                    animando = True
                elif botao_novo.clicado(pos):
                    maze = gerar_labirinto(LINHAS, COLUNAS)
                    resultado = None
                    explorados_visiveis = []
                    animando = False

        if animando and resultado is not None:
            if indice_animacao < len(resultado.explorados):
                explorados_visiveis.append(resultado.explorados[indice_animacao])
                indice_animacao += 1
            else:
                animando = False

        tela.fill(COR_FUNDO)

        titulo = fonte.render("Algoritmo:", True, COR_TEXTO)
        tela.blit(titulo, (20, 22))

        caminho_visivel = resultado.caminho if (resultado and not animando and resultado.encontrado) else []
        desenhar_tabuleiro(tela, maze, explorados_visiveis, caminho_visivel)

        y_rodape = MARGEM_TOPO + LINHAS * TAMANHO_CELULA + 10
        if resultado is not None:
            texto_stats = (
                f"Caminho: {len(resultado.caminho) if resultado.encontrado else 0} | "
                f"Expandidos: {resultado.expandidos} | Tempo: {resultado.tempo:.6f}s"
            )
        else:
            texto_stats = "Caminho: - | Expandidos: - | Tempo: -"
        stats_surf = fonte_pequena.render(texto_stats, True, COR_TEXTO)
        tela.blit(stats_surf, (MARGEM_LATERAL, y_rodape))

        desenhar_legenda(tela, fonte_pequena, y_rodape + 22)

        dropdown.desenhar(tela, fonte_pequena)
        botao_executar.desenhar(tela, fonte)
        botao_novo.desenhar(tela, fonte)

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
