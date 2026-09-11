"""
Classe Ranking: tela com os 10 melhores resultados (estilo arcade).

Mostra posição, nickname e pontuação em colunas alinhadas. A linha do
jogador atual pode ser destacada quando ele acabou de entrar no ranking.
"""
import math

import pygame

from ..settings import (
    LARGURA, ALTURA, NOME_JOGO, COR_MENU_TITULO, COR_MENU_DESTAQUE,
    COR_MENU_SOMBRA, COR_MENU_TEXTO, COR_SELVA_FUNDO, COR_BANANA,
)
from ..visual.tema import desenhar_moldura_selva, desenhar_botao_selva
from ..sons import tocar
from ..ranking import carregar_ranking, MAX_RANKING


class Ranking:
    def __init__(self, destaque_nick=None, destaque_score=None):
        self.destaque_nick = destaque_nick
        self.destaque_score = destaque_score
        self.fonte_titulo = pygame.font.SysFont(None, 72)
        self.fonte_posicao = pygame.font.SysFont(None, 34)
        self.fonte_nick = pygame.font.SysFont(None, 34)
        self.fonte_score = pygame.font.SysFont(None, 34)
        self.fonte_pequena = pygame.font.SysFont(None, 24)

        self.timer = 0
        self.botoes = []
        self.hover_anterior = None

    def atualizar(self):
        self.timer += 1

    def desenhar(self, tela):
        tela.fill(COR_SELVA_FUNDO)
        desenhar_moldura_selva(tela, self.timer)

        self._desenhar_titulo(tela)
        self._desenhar_lista(tela)
        self._desenhar_voltar(tela)

        espacador = self.fonte_pequena.render(
            "PRESSIONE ESC PARA VOLTAR", True, COR_MENU_TEXTO)
        tela.blit(espacador,
                  (LARGURA // 2 - espacador.get_width() // 2,
                   ALTURA - 22))

        assinatura = self.fonte_pequena.render(
            NOME_JOGO, True, COR_MENU_TEXTO)
        assinatura.set_alpha(150)
        tela.blit(assinatura, (12, ALTURA - 22))

    def _desenhar_titulo(self, tela):
        titulo = self.fonte_titulo.render("HIGH SCORES", True,
                                          COR_MENU_TITULO)
        sombra = self.fonte_titulo.render("HIGH SCORES", True,
                                          COR_MENU_SOMBRA)
        pulso = int(160 + 95 * (0.5 + 0.5 * math.sin(self.timer * 0.05)))
        titulo.set_alpha(pulso)
        sombra.set_alpha(int(pulso * 0.5))
        tela.blit(sombra, (LARGURA // 2 - titulo.get_width() // 2 + 3, 83))
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 80))

        top = self.fonte_pequena.render(
            f"TOP {MAX_RANKING}", True, COR_MENU_DESTAQUE)
        tela.blit(top, (LARGURA // 2 - top.get_width() // 2, 148))

    def _desenhar_lista(self, tela):
        rankings = carregar_ranking()
        if not rankings:
            vazio = self.fonte_nick.render(
                "AINDA NAO HA PONTUACOES", True, COR_MENU_TEXTO)
            tela.blit(vazio,
                      (LARGURA // 2 - vazio.get_width() // 2, 250))
            return

        y_inicio = 178
        espaco = 33
        for i, entrada in enumerate(rankings):
            self._desenhar_linha(tela, i + 1, entrada,
                                 y_inicio + i * espaco)

    def _desenhar_linha(self, tela, posicao, entrada, y):
        nick = entrada["nick"]
        score = entrada["score"]
        destaque = (nick == self.destaque_nick and
                    score == self.destaque_score)

        if destaque:
            fundo = pygame.Rect(LARGURA // 2 - 330, y - 4, 660, 34)
            pygame.draw.rect(tela, (60, 40, 20), fundo, border_radius=10)
            pygame.draw.rect(tela, COR_BANANA, fundo, 2, border_radius=10)
            cor = COR_MENU_DESTAQUE
            pulso = int(200 + 55 * (0.5 + 0.5 * math.sin(self.timer * 0.12)))
            flash = self.fonte_pequena.render("NOVO!", True, (pulso, pulso, 0))
            tela.blit(flash, (fundo.x + 10, fundo.y + 5))
        else:
            cor = COR_MENU_TEXTO

        num = self.fonte_posicao.render(f"{posicao:02d}", True,
                                        COR_MENU_DESTAQUE)
        tela.blit(num, (215, y))

        ban = self.fonte_pequena.render("^ ", True, COR_BANANA)
        if destaque:
            tela.blit(ban, (100, y + 4))

        nome = self.fonte_nick.render(nick, True, cor)
        tela.blit(nome, (LARGURA // 2 - nome.get_width() // 2, y))

        pontos = self.fonte_score.render(f"{score:,}".replace(",", "."),
                                         True, cor)
        tela.blit(pontos, (585 - pontos.get_width(), y))

    def _desenhar_voltar(self, tela):
        mouse = pygame.mouse.get_pos()
        self._botao(tela, "VOLTAR", self.fonte_pequena, ALTURA - 60, mouse,
                    "voltar", largura=200, altura=46)

        acao_hover = None
        for rect, acao in self.botoes:
            if rect.collidepoint(mouse):
                acao_hover = acao
                break
        if acao_hover is not None and acao_hover != self.hover_anterior:
            tocar("menu_hover")
        self.hover_anterior = acao_hover

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
                    tocar("menu_voltar")
                    return "voltar"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                tocar("menu_voltar")
                return "voltar"
        return None