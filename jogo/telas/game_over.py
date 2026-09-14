"""
Classe GameOver: tela de fim de jogo com estética de selva.

Mostra o nickname, a pontuação final e, caso o jogador tenha entrado no
Top 10 do ranking, destaca o novo recorde com a posição alcançada.
"""
import math

import pygame

from ..settings import (
    LARGURA, ALTURA, NOME_JOGO,
    COR_GAME_OVER, COR_MENU_DESTAQUE, COR_MENU_SOMBRA, COR_MENU_TEXTO,
    COR_MENU_TITULO, COR_SELVA_FUNDO, COR_BANANA,
)
from ..visual.tema import desenhar_moldura_selva, desenhar_botao_selva
from ..sons import tocar


class GameOver:
    def __init__(self, pontos, nick="MACACO", posicao_ranking=None):
        self.pontos = pontos
        self.nick = nick
        self.posicao_ranking = posicao_ranking  # 1 a 10, ou None

        self.fonte_titulo = pygame.font.SysFont(None, 90)
        self.fonte_nick = pygame.font.SysFont(None, 56)
        self.fonte_texto = pygame.font.SysFont(None, 36)
        self.fonte_record = pygame.font.SysFont(None, 44)
        self.fonte_pequena = pygame.font.SysFont(None, 28)

        self.timer = 0
        self.botoes = []     # (rect, acao) desenhados no último frame
        self.hover_anterior = None

    def atualizar(self):
        self.timer += 1

    def desenhar(self, tela):
        tela.fill(COR_SELVA_FUNDO)
        desenhar_moldura_selva(tela, self.timer)

        mouse = pygame.mouse.get_pos()
        self.botoes = []

        # layout uniforme (com ou sem recorde — os botões ficam sempre
        # nas mesmas posições, evitando a sensação de informações
        # empilhadas)
        self._botao(tela, "REINICIAR", self.fonte_texto, 560, mouse,
                    "reiniciar", largura=340, altura=60)
        self._botao(tela, "SAIR", self.fonte_texto, 635, mouse, "sair",
                    largura=240, altura=50)

        acao_hover = None
        for rect, acao in self.botoes:
            if rect.collidepoint(mouse):
                acao_hover = acao
                break
        if acao_hover is not None and acao_hover != self.hover_anterior:
            tocar("menu_hover")
        self.hover_anterior = acao_hover

        self._desenhar_titulo(tela)
        self._desenhar_pontuacao(tela)
        self._desenhar_assinatura(tela)

    def _desenhar_assinatura(self, tela):
        rodape = self.fonte_pequena.render(
            NOME_JOGO, True, COR_MENU_TEXTO)
        rodape.set_alpha(150)
        tela.blit(rodape,
                  (LARGURA // 2 - rodape.get_width() // 2, ALTURA - 30))

    def _desenhar_titulo(self, tela):
        titulo = self.fonte_titulo.render("GAME OVER", True, COR_GAME_OVER)
        sombra = self.fonte_titulo.render("GAME OVER", True, COR_MENU_SOMBRA)
        pulso = int(150 + 105 * (0.5 + 0.5 * math.sin(self.timer * 0.05)))
        titulo.set_alpha(pulso)
        sombra.set_alpha(int(pulso * 0.5))
        flut = int(math.sin(self.timer * 0.04) * 3)
        tela.blit(sombra, (LARGURA // 2 - titulo.get_width() // 2 + 4,
                           74 + flut))
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2,
                           70 + flut))

    def _desenhar_pontuacao(self, tela):
        # nickname em destaque
        nick_surf = self.fonte_nick.render(self.nick, True,
                                           COR_MENU_DESTAQUE)
        sombra_nick = self.fonte_nick.render(self.nick, True,
                                             COR_MENU_SOMBRA)
        tela.blit(sombra_nick,
                  (LARGURA // 2 - nick_surf.get_width() // 2 + 3, 213))
        tela.blit(nick_surf,
                  (LARGURA // 2 - nick_surf.get_width() // 2, 210))

        pontos_texto = self.fonte_texto.render(
            f"SCORE: {self.pontos}", True, COR_MENU_TEXTO)
        tela.blit(pontos_texto,
                  (LARGURA // 2 - pontos_texto.get_width() // 2, 290))

        if self.posicao_ranking is not None:
            self._desenhar_record(tela)
        else:
            self._desenhar_frase_motivacional(tela)

    def _desenhar_record(self, tela):
        """Painel com destaque para novo recorde."""
        cx = LARGURA // 2
        # painel marrom discreto
        rect_painel = pygame.Rect(0, 0, 460, 82)
        rect_painel.center = (cx, 410)
        pygame.draw.rect(tela, (50, 34, 20), rect_painel, border_radius=12)
        pygame.draw.rect(tela, COR_BANANA, rect_painel, 2,
                         border_radius=12)

        # label "NOVO!" no canto superior esquerdo do painel
        pulso = int(170 + 85 * (0.5 + 0.5 * math.sin(self.timer * 0.12)))
        novo = self.fonte_pequena.render("NOVO!", True, (pulso, pulso, 0))
        tela.blit(novo, (rect_painel.x + 14, rect_painel.y + 8))

        # texto principal do recorde
        recorde = self.fonte_record.render(
            "NEW HIGH SCORE!", True, COR_BANANA)
        tela.blit(recorde, (cx - recorde.get_width() // 2,
                            rect_painel.y + 14))

        posicao = self.fonte_texto.render(
            f"POSITION #{self.posicao_ranking}", True, COR_MENU_TITULO)
        tela.blit(posicao, (cx - posicao.get_width() // 2,
                            rect_painel.y + 52))

    def _desenhar_frase_motivacional(self, tela):
        """Pequena mensagem quando não há novo recorde."""
        pulso = int(120 + 135 * (0.5 + 0.5 * math.sin(self.timer * 0.06)))
        texto = self.fonte_pequena.render(
            "TENTE NOVAMENTE!", True, COR_MENU_TITULO)
        texto.set_alpha(pulso)
        tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 408))

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
