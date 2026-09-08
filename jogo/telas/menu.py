"""
Classe Menu: tela inicial do jogo com estética de selva.

Mantém a identidade tropical do macaco: folhas nas bordas, cipós,
bananas e botões em placas de madeira.
"""
import math

import pygame

from ..settings import (
    LARGURA, ALTURA,
    COR_MENU_TITULO, COR_MENU_DESTAQUE, COR_MENU_SOMBRA, COR_MENU_TEXTO,
    COR_SELVA_FUNDO,
)
from ..visual.tema import desenhar_moldura_selva, desenhar_botao_selva


class Menu:
    def __init__(self):
        self.fonte_titulo = pygame.font.SysFont(None, 80)
        self.fonte_texto = pygame.font.SysFont(None, 32)
        self.fonte_pequena = pygame.font.SysFont(None, 26)

        self.timer = 0
        self.botoes = []     # (rect, acao) desenhados no último frame

    def atualizar(self):
        self.timer += 1

    def desenhar(self, tela):
        tela.fill(COR_SELVA_FUNDO)
        desenhar_moldura_selva(tela, self.timer)

        mouse = pygame.mouse.get_pos()
        self.botoes = []

        # botões (placa de madeira), hover animado
        self._botao(tela, "JOGAR", self.fonte_texto, 300, mouse, "iniciar",
                    largura=320, altura=62)
        self._botao(tela, "SAIR", self.fonte_texto, 390, mouse, "sair",
                    largura=230, altura=52)

        # controles (dica), em texto discreto
        controles = ["W A S D - Mover", "ESPACO - Atirar"]
        rotulo = self.fonte_pequena.render("CONTROLES", True, COR_MENU_TEXTO)
        tela.blit(rotulo, (LARGURA // 2 - rotulo.get_width() // 2, 476))
        y = 502
        for linha in controles:
            render = self.fonte_pequena.render(linha, True, COR_MENU_TEXTO)
            tela.blit(render, (LARGURA // 2 - render.get_width() // 2, y))
            y += 24

        # título (pulsa e flutua levemente)
        self._desenhar_titulo(tela)

    def _desenhar_titulo(self, tela):
        titulo = self.fonte_titulo.render("MACACUQUITO", True, COR_MENU_TITULO)
        sombra = self.fonte_titulo.render(
            "MACACUQUITO", True, COR_MENU_SOMBRA)
        pulso = int(150 + 105 * (0.5 + 0.5 * math.sin(self.timer * 0.05)))
        titulo.set_alpha(pulso)
        sombra.set_alpha(int(pulso * 0.5))
        flut = int(math.sin(self.timer * 0.04) * 4)
        tela.blit(sombra, (LARGURA // 2 - titulo.get_width() // 2 + 3,
                           83 + flut))
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 80 + flut))

        louco = self.fonte_titulo.render("LOUCO", True, COR_MENU_DESTAQUE)
        sombra_louco = self.fonte_titulo.render(
            "LOUCO", True, COR_MENU_SOMBRA)
        tela.blit(sombra_louco, (LARGURA // 2 - louco.get_width() // 2 + 3,
                                 163 + flut))
        tela.blit(louco, (LARGURA // 2 - louco.get_width() // 2, 160 + flut))

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
                return "iniciar"
            if event.key == pygame.K_ESCAPE:
                return "sair"
        return None