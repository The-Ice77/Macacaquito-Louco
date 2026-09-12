"""
Classe Nickname: tela de entrada do nickname antes de iniciar a partida.

Permite até 8 caracteres (letras e números, convertidos para maiúsculas),
com cursor piscando e confirmação via Enter. Um nickname vazio não é aceito.
"""
import pygame

from ..settings import (
    LARGURA, COR_MENU_TITULO, COR_MENU_SOMBRA,
    COR_MENU_TEXTO, COR_MADEIRA, COR_MADEIRA_CLARA, COR_MADEIRA_BORDA,
    COR_MADEIRA_TEXTO, COR_SELVA_FUNDO, COR_BANANA,
)
from ..visual.tema import (
    desenhar_moldura_selva, desenhar_botao_selva, desenhar_macaco,
)
from ..sons import tocar


class Nickname:
    def __init__(self):
        self.fonte_titulo = pygame.font.SysFont(None, 64)
        self.fonte_texto = pygame.font.SysFont(None, 52)
        self.fonte_pequena = pygame.font.SysFont(None, 26)

        self.texto = ""
        self.timer = 0
        self.timer_celebracao = 0
        self.botoes = []          # (rect, acao) desenhados no último frame
        self.hover_anterior = None

    def atualizar(self):
        self.timer += 1
        if self.timer_celebracao > 0:
            self.timer_celebracao -= 1

    def celebrar(self):
        """Macaco comemora ao iniciar uma nova partida."""
        self.timer_celebracao = 45

    def desenhar(self, tela):
        tela.fill(COR_SELVA_FUNDO)
        desenhar_moldura_selva(tela, self.timer)

        titulo = self.fonte_titulo.render(
            "ENTRE COM SEU NICK", True, COR_MENU_TITULO)
        sombra = self.fonte_titulo.render(
            "ENTRE COM SEU NICK", True, COR_MENU_SOMBRA)
        tela.blit(sombra, (LARGURA // 2 - titulo.get_width() // 2 + 3, 103))
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 100))

        self._desenhar_campo(tela)
        self._desenhar_confirmar(tela)
        self._desenhar_dica(tela)

        # macaco decorativo no canto, comemorando ao iniciar a partida
        if self.timer_celebracao > 0:
            desenhar_macaco(tela, 78, 420, self.timer,
                            olhar_x=LARGURA // 2, celebrar=True)
        else:
            desenhar_macaco(tela, 78, 420, self.timer,
                            olhar_x=LARGURA // 2)

    def _desenhar_campo(self, tela):
        """Campo de texto em madeira, com cursor piscando."""
        centro_x = LARGURA // 2
        y = 260
        largura = 420
        altura = 78

        rect = pygame.Rect(0, 0, largura, altura)
        rect.center = (centro_x, y)
        pygame.draw.rect(tela, (58, 36, 20), rect.move(4, 6),
                         border_radius=14)
        pygame.draw.rect(tela, COR_MADEIRA, rect, border_radius=14)
        pygame.draw.rect(tela, COR_MADEIRA_CLARA, rect, 2, border_radius=14)
        pygame.draw.rect(tela, COR_MADEIRA_BORDA, rect, 4, border_radius=14)

        texto = self.fonte_texto.render(self.texto, True, COR_MADEIRA_TEXTO)
        largura_texto = texto.get_width()
        centro_y = y - texto.get_height() // 2
        x_texto = centro_x - (largura_texto + 6) // 2
        tela.blit(texto, (x_texto, centro_y))

        # cursor piscando ao lado do texto
        if (self.timer // 30) % 2 == 0:
            pygame.draw.line(tela, COR_BANANA,
                             (x_texto + largura_texto + 4, centro_y + 4),
                             (x_texto + largura_texto + 4,
                              centro_y + texto.get_height() - 4), 4)

        contador = self.fonte_pequena.render(
            f"{len(self.texto)}/8", True, COR_MENU_TEXTO)
        tela.blit(contador, (rect.right - contador.get_width() - 12,
                             rect.bottom - contador.get_height() - 8))

    def _desenhar_confirmar(self, tela):
        """Botão de confirmar (Enter) e subtítulo destacado."""
        mouse = pygame.mouse.get_pos()
        self.botoes = []
        self._botao(tela, "CONFIRMAR", self.fonte_pequena, 440, mouse,
                    "confirmar", largura=240, altura=48)
        self._desenhar_voltar_dica(tela)

    def _desenhar_voltar_dica(self, tela):
        dica = self.fonte_pequena.render(
            "ENTER - CONFIRMAR   |   ESC - VOLTAR", True, COR_MENU_TEXTO)
        tela.blit(dica, (LARGURA // 2 - dica.get_width() // 2, 505))

    def _desenhar_dica(self, tela):
        linhas = [
            "LETRAS E NUMEROS - ate 8 caracteres",
            "O nickname e salvo no ranking",
        ]
        y = 556
        for linha in linhas:
            render = self.fonte_pequena.render(linha, True, COR_MENU_TEXTO)
            tela.blit(render, (LARGURA // 2 - render.get_width() // 2, y))
            y += 24

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
                    return self._confirmar()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return self._confirmar()
            if event.key == pygame.K_BACKSPACE:
                if self.texto:
                    self.texto = self.texto[:-1]
                    tocar("menu_hover")
                return None
            if event.key == pygame.K_ESCAPE:
                tocar("menu_voltar")
                return "voltar"
            if len(self.texto) < 8 and event.unicode:
                char = event.unicode
                if char.isascii() and char.isalnum():
                    self.texto += char.upper()
                    tocar("menu_hover")
        return None

    def _confirmar(self):
        """Confirma o nickname (bloqueado se vazio)."""
        if not self.texto:
            return None
        tocar("menu_confirmar")
        return "confirmar"