"""
Classe Pausa: menu aberto durante a gameplay para continuar, reiniciar ou sair.

Usa a mesma estética de selva dos outros menus, desenhada sobre uma camada
escura que mantém a partida congelada ao fundo.
"""
import math

import pygame

from ..settings import LARGURA, ALTURA, COR_MENU_TITULO, COR_MENU_TEXTO
from ..visual.tema import desenhar_botao_selva
from ..sons import tocar
from .navegacao import Navegacao


class Pausa(Navegacao):
    def __init__(self):
        self.fonte_titulo = pygame.font.SysFont(None, 70)
        self.fonte_texto = pygame.font.SysFont(None, 32)
        self.fonte_dica = pygame.font.SysFont(None, 24)

        self.timer = 0
        self.botoes = []     # (rect, acao) desenhados no último frame
        self.hover_anterior = None
        self._iniciar_navegacao("continuar")

    def atualizar(self):
        self.timer += 1

    def desenhar(self, tela):
        # camada escura translúcida sobre a partida congelada
        escurecer = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        escurecer.fill((0, 0, 0, 170))
        tela.blit(escurecer, (0, 0))

        titulo = self.fonte_titulo.render("PAUSA", True, COR_MENU_TITULO)
        pulso = int(200 + 55 * (0.5 + 0.5 * math.sin(self.timer * 0.05)))
        titulo.set_alpha(pulso)
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 100))

        mouse = pygame.mouse.get_pos()
        self.botoes = []

        self._botao(tela, "CONTINUAR", self.fonte_texto, 290, mouse,
                    "continuar", largura=300, altura=55)
        self._botao(tela, "REINICIAR", self.fonte_texto, 378, mouse,
                    "reiniciar", largura=300, altura=55)
        self._botao(tela, "OPCOES", self.fonte_texto, 466, mouse, "config",
                    largura=260, altura=52)
        self._botao(tela, "SAIR", self.fonte_texto, 550, mouse, "sair",
                    largura=230, altura=50)

        acao_hover = None
        for rect, acao in self.botoes:
            if rect.collidepoint(mouse):
                acao_hover = acao
                break
        if acao_hover is not None and acao_hover != self.hover_anterior:
            tocar("menu_hover")
        self.hover_anterior = acao_hover
        self._sincronizar_mouse(mouse)

        dica = "SETAS ou W A S D - Navegar    |    ENTER - Confirmar"
        texto = self.fonte_dica.render(dica, True, COR_MENU_TEXTO)
        texto.set_alpha(150)
        tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 620))

    def _botao(self, tela, texto, fonte, y, mouse, acao,
               largura=300, altura=56):
        rect = pygame.Rect(0, 0, largura, altura)
        rect.center = (LARGURA // 2, y)
        hover = (rect.collidepoint(mouse)
                 or self._esta_selecionado(acao))
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
            acao = self._navegar_teclado(event)
            if acao is not None:
                return acao
            if event.key == pygame.K_ESCAPE:
                return "continuar"
        return None