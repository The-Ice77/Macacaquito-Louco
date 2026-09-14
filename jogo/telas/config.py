"""
Classe Configuracoes: menu de opções com estética de selva.

Atualmente controla o volume do som (geral e dos efeitos) por meio de
barras de volume clicáveis. Novas opções podem ser adicionadas depois na
lista `self.itens`, seguindo o formato (rotulo, obter, definir), sem mexer
no restante da tela.
"""
import pygame

from ..settings import (
    LARGURA, COR_MENU_TITULO, COR_MENU_DESTAQUE, COR_MENU_SOMBRA,
    COR_MENU_TEXTO, COR_SELVA_FUNDO,
    COR_MADEIRA_BORDA, COR_BANANA, COR_BANANA_PONTA,
)
from ..visual.tema import desenhar_moldura_selva, desenhar_botao_selva
from ..sons import (
    tocar, volume_mestre, set_volume_mestre,
    volume_efeitos, set_volume_efeitos,
)

_PASSO_VOLUME = 0.05
_LARGURA_BARRA = 480
_ALTURA_BARRA = 18
_RAIO_KNOB = 12
_ESPACO_ITENS = 130


class Configuracoes:
    def __init__(self):
        self.fonte_titulo = pygame.font.SysFont(None, 70)
        self.fonte_texto = pygame.font.SysFont(None, 32)
        self.fonte_pequena = pygame.font.SysFont(None, 24)

        # Cada item é uma opção ajustável com uma barra de volume.
        self.itens = [
            {
                "rotulo": "VOLUME GERAL",
                "obter": volume_mestre,
                "definir": set_volume_mestre,
            },
            {
                "rotulo": "EFEITOS SONOROS",
                "obter": volume_efeitos,
                "definir": set_volume_efeitos,
            },
        ]

        self.timer = 0
        self.botoes = []          # (rect, acao) desenhados no último frame
        self.hover_anterior = None
        self.indice = 0           # item selecionado pelo teclado
        self.retorno = "menu"     # estado para onde voltar ao sair

    def atualizar(self):
        self.timer += 1

    def desenhar(self, tela):
        tela.fill(COR_SELVA_FUNDO)
        desenhar_moldura_selva(tela, self.timer)

        titulo = self.fonte_titulo.render("OPCOES", True, COR_MENU_TITULO)
        sombra = self.fonte_titulo.render("OPCOES", True, COR_MENU_SOMBRA)
        tela.blit(sombra, (LARGURA // 2 - titulo.get_width() // 2 + 3, 73))
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 70))

        mouse = pygame.mouse.get_pos()
        self.botoes = []

        for indice, item in enumerate(self.itens):
            self._desenhar_item(tela, indice, item, mouse)

        self._botao(tela, LARGURA // 2, "VOLTAR", self.fonte_texto, 590,
                    mouse, "voltar", largura=230, altura=52)

        acao_hover = None
        for rect, acao in self.botoes:
            if rect.collidepoint(mouse):
                acao_hover = acao
                break
        if acao_hover is not None and acao_hover != self.hover_anterior:
            tocar("menu_hover")
        self.hover_anterior = acao_hover

    def _desenhar_item(self, tela, indice, item, mouse):
        centro = LARGURA // 2
        y_inicio = 250 + indice * _ESPACO_ITENS

        cor_rotulo = (COR_MENU_DESTAQUE if indice == self.indice
                      else COR_MENU_TEXTO)
        rotulo = self.fonte_texto.render(item["rotulo"], True, cor_rotulo)
        tela.blit(rotulo, (centro - rotulo.get_width() // 2, y_inicio))

        valor = item["obter"]()
        y_barra = y_inicio + 44
        self._desenhar_barra(tela, indice, valor, centro, y_barra)

        texto_valor = self.fonte_pequena.render(
            f"{round(valor * 100)}%", True, COR_MENU_TEXTO)
        tela.blit(texto_valor,
                  (centro - texto_valor.get_width() // 2, y_barra + 30))

    def _desenhar_barra(self, tela, indice, valor, centro, y):
        """Barra de volume estilo trilho de madeira com preenchimento banana."""
        x = centro - _LARGURA_BARRA // 2
        trilho = pygame.Rect(x, y, _LARGURA_BARRA, _ALTURA_BARRA)

        # trilho de madeira escura
        pygame.draw.rect(tela, (48, 30, 18), trilho, border_radius=9)
        interno = trilho.inflate(-8, -8)
        pygame.draw.rect(tela, COR_MADEIRA_BORDA, interno, border_radius=5)
        pygame.draw.rect(tela, COR_MADEIRA_BORDA, trilho, 2, border_radius=9)

        # preenchimento (banana) até o valor atual
        larg_fill = int((_LARGURA_BARRA - 4) * valor)
        if larg_fill > 0:
            preench = pygame.Rect(x + 2, y + 2,
                                  max(10, larg_fill), _ALTURA_BARRA - 4)
            pygame.draw.rect(tela, COR_BANANA, preench, border_radius=7)
            pygame.draw.line(tela, COR_BANANA_PONTA,
                             (preench.x + 4, preench.y + 4),
                             (preench.right - 4, preench.y + 4), 2)

        # botão deslizante (knob) no final do preenchimento
        knob_x = max(x, min(x + _LARGURA_BARRA, x + larg_fill))
        knob_y = y + _ALTURA_BARRA // 2
        pygame.draw.circle(tela, (255, 245, 210), (knob_x, knob_y),
                           _RAIO_KNOB)
        pygame.draw.circle(tela, COR_MADEIRA_BORDA, (knob_x, knob_y),
                           _RAIO_KNOB, 3)
        if indice == self.indice:
            pygame.draw.circle(tela, COR_MENU_DESTAQUE, (knob_x, knob_y),
                               _RAIO_KNOB - 5)

        self.botoes.append((trilho, f"volume_{indice}"))
        knob_rect = pygame.Rect(knob_x - _RAIO_KNOB, knob_y - _RAIO_KNOB,
                                _RAIO_KNOB * 2, _RAIO_KNOB * 2)
        self.botoes.append((knob_rect, f"volume_{indice}"))

    def _botao(self, tela, x, texto, fonte, y, mouse, acao,
               largura=300, altura=56):
        rect = pygame.Rect(0, 0, largura, altura)
        rect.center = (x, y)
        hover = rect.collidepoint(mouse)
        desenhar_botao_selva(
            tela, x, y, largura, altura, texto, fonte, self.timer, hover)
        self.botoes.append((rect, acao))

    def tratar_evento(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, acao in self.botoes:
                if rect.collidepoint(event.pos):
                    if acao == "voltar":
                        return acao
                    if acao.startswith("volume_"):
                        self._ajustar_por_barra(int(acao.split("_")[1]),
                                                event.pos[0])
                    return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "voltar"
            if event.key in (pygame.K_UP, pygame.K_w):
                self.indice = (self.indice - 1) % len(self.itens)
                tocar("menu_hover")
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.indice = (self.indice + 1) % len(self.itens)
                tocar("menu_hover")
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self._ajustar(self.indice, -_PASSO_VOLUME)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self._ajustar(self.indice, _PASSO_VOLUME)
        return None

    def _ajustar_por_barra(self, indice, x_mouse):
        """Define o volume conforme a posição do clique na barra."""
        item = self.itens[indice]
        x0 = LARGURA // 2 - _LARGURA_BARRA // 2
        novo = max(0.0, min(1.0, round((x_mouse - x0) / _LARGURA_BARRA, 2)))
        item["definir"](novo)
        tocar("menu_hover")

    def _ajustar(self, indice, delta):
        item = self.itens[indice]
        atual = item["obter"]()
        novo = max(0.0, min(1.0, round(atual + delta, 2)))
        item["definir"](novo)
        tocar("menu_hover")