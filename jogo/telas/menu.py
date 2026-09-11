"""
Classe Menu: tela inicial do jogo com estética de selva.

Mantém a identidade tropical do macaco: folhas nas bordas, cipós,
bananas e botões em placas de madeira. Hierarquia visual:
TÍTULO > BOTÕES > PERSONAGEM > DECORAÇÃO.
"""
import math

import pygame

from ..settings import (
    LARGURA, ALTURA,
    COR_BANANA, COR_MENU_TEXTO, COR_MENU_SOMBRA, COR_SELVA_FUNDO,
)
from ..visual.tema import (
    desenhar_moldura_selva, desenhar_botao_selva, desenhar_macaco,
    banana_surface,
)
from ..sons import tocar


SIMBOLOS = {
    "iniciar": "banana",
    "ranking": "estrela",
    "config": "engrenagem",
    "sair": "folha",
}


class Menu:
    def __init__(self):
        self.fonte_operacao = pygame.font.SysFont(None, 40)
        self.fonte_banana = pygame.font.SysFont(None, 96)
        self.fonte_texto = pygame.font.SysFont(None, 32)
        self.fonte_pequena = pygame.font.SysFont(None, 26)

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

        # botões (placa de madeira), hover animado com ícone
        self._botao(tela, "JOGAR", self.fonte_texto, 256, mouse, "iniciar",
                    largura=320, altura=62, simbolo=SIMBOLOS["iniciar"])
        self._botao(tela, "RANKING", self.fonte_texto, 344, mouse,
                    "ranking", largura=260, altura=56,
                    simbolo=SIMBOLOS["ranking"])
        self._botao(tela, "OPCOES", self.fonte_texto, 430, mouse, "config",
                    largura=260, altura=56, simbolo=SIMBOLOS["config"])
        self._botao(tela, "SAIR", self.fonte_texto, 512, mouse, "sair",
                    largura=230, altura=50, simbolo=SIMBOLOS["sair"])

        acao_hover = None
        for rect, acao in self.botoes:
            if rect.collidepoint(mouse):
                acao_hover = acao
                break
        if acao_hover is not None and acao_hover != self.hover_anterior:
            tocar("menu_hover")
        self.hover_anterior = acao_hover

        # controles (dica), em texto discreto
        controles = "W A S D - Mover    |    ESPACO - Atirar"
        rotulo = self.fonte_pequena.render(controles, True, COR_MENU_TEXTO)
        tela.blit(rotulo, (LARGURA // 2 - rotulo.get_width() // 2, 570))

        # macaco com pequenas animações na lateral (segue o mouse com os olhos)
        desenhar_macaco(tela, 96, 516, self.timer, olhar_x=mouse[0])

        # título por último (elemento de maior destaque)
        self._desenhar_titulo(tela)

    def _desenhar_titulo(self, tela):
        # entrada animada: o título desliza do topo e faz fade
        t = min(1.0, self.timer / 30)
        suave = t * t * (3 - 2 * t)
        desloca = int((1 - suave) * 70)
        alvo_alpha = int(255 * suave)

        flut_op = int(math.sin(self.timer * 0.04) * 2)
        flut_ban = int(math.sin(self.timer * 0.05) * 3)

        # --- OPERAÇÃO (linha discreta) ---
        operacao = self.fonte_operacao.render("OPERAÇÃO", True, COR_MENU_TEXTO)
        sombra_op = self.fonte_operacao.render(
            "OPERAÇÃO", True, COR_MENU_SOMBRA)
        x_op = LARGURA // 2 - operacao.get_width() // 2
        y_op = 60 + flut_op - desloca
        sombra_op.set_alpha(alvo_alpha)
        operacao.set_alpha(int(alvo_alpha * 0.9))
        tela.blit(sombra_op, (x_op + 2, y_op + 2))
        tela.blit(operacao, (x_op, y_op))

        # --- BANANA (maior destaque, amarelo) ---
        banana = self.fonte_banana.render("BANANA", True, COR_BANANA)
        sombra_b = self.fonte_banana.render("BANANA", True, COR_MENU_SOMBRA)
        brilho_b = self.fonte_banana.render("BANANA", True, (210, 255, 140))
        pulso = 0.5 + 0.5 * math.sin(self.timer * 0.03)
        brilho_b.set_alpha(int(18 + 32 * pulso))

        x_b = LARGURA // 2 - banana.get_width() // 2
        y_b = 102 + flut_ban - desloca
        tela.blit(sombra_b, (x_b + 4, y_b + 4))
        tela.blit(brilho_b, (x_b, y_b))
        tela.blit(banana, (x_b, y_b))

        # bananas decorativas ao lado do título (balançam, discretas)
        lado = banana_surface(12)
        ang = math.sin(self.timer * 0.06) * 14 + 20
        esq = pygame.transform.rotozoom(lado, ang, 1)
        dir_ = pygame.transform.rotozoom(lado, -ang, 1)
        esq.set_alpha(190)
        dir_.set_alpha(190)
        y_lado = y_b + banana.get_height() // 2
        tela.blit(esq, (x_b - 48 - esq.get_width() // 2,
                        y_lado - esq.get_height() // 2))
        tela.blit(dir_, (x_b + banana.get_width() + 48 - dir_.get_width() // 2,
                         y_lado - dir_.get_height() // 2))

    def _botao(self, tela, texto, fonte, y, mouse, acao,
               largura=300, altura=56, simbolo=None):
        rect = pygame.Rect(0, 0, largura, altura)
        rect.center = (LARGURA // 2, y)
        hover = rect.collidepoint(mouse)
        desenhar_botao_selva(
            tela, LARGURA // 2, y, largura, altura, texto,
            fonte, self.timer, hover, simbolo=simbolo)
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