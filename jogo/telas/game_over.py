"""
Classe GameOver: tela de fim de jogo com estética de selva.

Mesma identidade do Menu: folhas, cipós e bananas como moldura, com
botões em placas de madeira para reiniciar ou sair.
"""
import math

import pygame

from ..settings import (
    LARGURA, ALTURA,
    COR_GAME_OVER, COR_MENU_DESTAQUE, COR_MENU_SOMBRA, COR_MENU_TEXTO,
    COR_SELVA_FUNDO,
)
from ..visual.tema import desenhar_moldura_selva, desenhar_botao_selva


class GameOver:
    def __init__(self, pontos):
        self.pontos = pontos
        self.fonte_titulo = pygame.font.SysFont(None, 90)
        self.fonte_texto = pygame.font.SysFont(None, 36)
        self.fonte_pequena = pygame.font.SysFont(None, 28)

        self.timer = 0
        self.botoes = []     # (rect, acao) desenhados no último frame

    def atualizar(self):
        self.timer += 1

    def desenhar(self, tela):
        tela.fill(COR_SELVA_FUNDO)
        desenhar_moldura_selva(tela, self.timer)

        mouse = pygame.mouse.get_pos()
        self.botoes = []

        self._botao(tela, "REINICIAR", self.fonte_texto, 340, mouse,
                    "reiniciar", largura=320, altura=60)
        self._botao(tela, "SAIR", self.fonte_texto, 420, mouse, "sair",
                    largura=230, altura=50)

        dica = self.fonte_pequena.render(
            "Obrigado por jogar!", True, COR_MENU_TEXTO)
        tela.blit(dica, (LARGURA // 2 - dica.get_width() // 2, 505))

        self._desenhar_titulo(tela)

    def _desenhar_titulo(self, tela):
        titulo = self.fonte_titulo.render("GAME OVER", True, COR_GAME_OVER)
        sombra = self.fonte_titulo.render("GAME OVER", True, COR_MENU_SOMBRA)
        pulso = int(150 + 105 * (0.5 + 0.5 * math.sin(self.timer * 0.05)))
        titulo.set_alpha(pulso)
        sombra.set_alpha(int(pulso * 0.5))
        flut = int(math.sin(self.timer * 0.04) * 5)
        tela.blit(sombra, (LARGURA // 2 - titulo.get_width() // 2 + 4,
                           94 + flut))
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2,
                           90 + flut))

        pontos_texto = self.fonte_texto.render(
            f"PONTUACAO FINAL: {self.pontos}", True, COR_MENU_DESTAQUE)
        tela.blit(pontos_texto,
                  (LARGURA // 2 - pontos_texto.get_width() // 2, 235))

    def _botao(self, tela, texto, fonte, y, mouse, acao,
               largura=300, altura=56):
        rect = pygame.Rect(0, 0, largura, altura)
        rect.center = (LARGURA // 2, y)
        hover = rect.collidepoint(mouse)
        desenhar_botao_selva(
            tela, LARGURA // 2, y, largura, altura, texto,
            fonte, self.timer, hover)
        self.botoes.append((rect, acao))

    def tratar_evento(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, acao in self.botoes:
                if rect.collidepoint(event.pos):
                    return acao
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "reiniciar"
            if event.key == pygame.K_ESCAPE:
                return "sair"
        return None