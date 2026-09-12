"""
Classes de power-ups: itens coletáveis que dão vantagens ao jogador.

Cada power-up cai do topo da tela devagar, é coletado ao tocar o jogador
e desaparece se sair da tela. Enquanto está na tela, flutua levemente,
gira e pulsa com um anel de brilho.
"""
import math
import random

import pygame

from .entidade import Entidade, escalar
from ..settings import (
    ALTURA, POWERUP_VELOCIDADE,
    FATOR_ESCALA_POWERUP,
    COR_FOLHA, COR_BANANA_NOVA, COR_BANANA_PONTA,
    COR_MORANGO, COR_MORANGO_ESC,
    COR_ABACAXI, COR_ABACAXI_ESC,
    COR_MELANCIA_CASCA_ESC, COR_MELANCIA_POLPA,
    COR_MACA, COR_MACA_ESC,
    POWERUP_DURACAO_TURBO, POWERUP_DURACAO_TIRO_DUPLO,
    POWERUP_DURACAO_ESCUDO, POWERUP_DURACAO_MEGA_TIRO,
    POWERUP_BONUS_PONTOS,
)


def _pequena_banana(cor=COR_BANANA_NOVA, ponta=COR_BANANA_PONTA):
    """Banana-crescente mini, usada nos power-ups (tiro duplo e dourada)."""
    s = pygame.Surface((20, 14), pygame.SRCALPHA)
    esc = tuple(max(0, int(c * 0.6)) for c in cor)
    pygame.draw.arc(s, esc, (2, 3, 16, 9), 0.2, math.pi - 0.2, 4)
    pygame.draw.arc(s, cor, (3, 4, 14, 7), 0.3, math.pi - 0.3, 3)
    pygame.draw.circle(s, ponta, (3, 7), 2)
    pygame.draw.circle(s, ponta, (17, 8), 2)
    pygame.draw.circle(s, tuple(min(255, int(c * 1.8)) for c in cor),
                       (10, 6), 1)
    return s


class PowerUp(Entidade):
    """Base comum: fruta colorida com um símbolo identificador."""

    def __init__(self, x, y):
        super().__init__(x, y, POWERUP_VELOCIDADE)
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self._desenhar()
        self.icon = self.image.copy()   # ícone estático (base)
        self.fase = random.uniform(0, math.tau)

    def _desenhar(self):
        # sobrescrito por cada tipo
        pass

    def _efeito_dinamico(self, alvo, fase):
        """Animação extra desenhada atrás da fruta (sobrescrita por tipo)."""
        pass

    def aplicar(self, jogador):
        """Aplica o efeito. Retorna pontos extras quando houver."""
        return None

    def update(self):
        self.fase += 1
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA:
            self.kill()
            return

        # flutuação vertical do ícone dentro da superfície
        flut = int(math.sin(self.fase * 0.09) * 3)
        alvo = pygame.Surface((30, 30), pygame.SRCALPHA)
        # animação própria (pulso/brilhos) desenhada atrás da fruta
        self._efeito_dinamico(alvo, self.fase)
        alvo.blit(self.icon, (0, flut))

        # anel de brilho que pulsa + pontinho girando (sensação de rotação)
        anel = pygame.Surface((30, 30), pygame.SRCALPHA)
        raio_anel = int(15 + math.sin(self.fase * 0.1) * 2)
        pygame.draw.circle(anel, (255, 255, 255), (15, 15), raio_anel, 1)
        anel.set_alpha(int(60 + 60 * (0.5 + 0.5 * math.sin(self.fase * 0.1))))
        orbit = self.fase * 0.12
        ox = math.cos(orbit) * (raio_anel + 1)
        oy = math.sin(orbit) * (raio_anel + 1)
        pygame.draw.circle(anel, (255, 255, 255),
                           (int(15 + ox), int(15 + oy)), 1)
        alvo.blit(anel, (0, 0))

        # amplia o quadro completo (icone + animações) proporcionalmente
        centro = self.rect.center
        self.image = escalar(alvo, FATOR_ESCALA_POWERUP)
        self.rect = self.image.get_rect(center=centro)


class BananaTurbo(PowerUp):
    """Morango veloz: linhas de velocidade + polpa com sementes.

    Aumenta temporariamente a velocidade do jogador."""

    def _desenhar(self):
        # rastro de velocidade (atrás do morango)
        pygame.draw.line(self.image, (255, 255, 255, 90), (3, 24), (10, 17), 1)
        pygame.draw.line(self.image, (255, 255, 255, 60), (1, 27), (7, 22), 1)
        # corpo do morango (triangular arredondado)
        pontos = [(9, 7), (21, 7), (24, 12), (23, 17), (15, 24), (7, 17), (6, 12)]
        pygame.draw.polygon(self.image, COR_MORANGO, pontos)
        pygame.draw.polygon(self.image, COR_MORANGO_ESC, pontos, 1)
        # sementinhas creme
        for sx, sy in ((11, 11), (15, 10), (19, 12), (13, 16), (18, 17)):
            pygame.draw.circle(self.image, (255, 235, 190), (sx, sy), 1)
        # coroa verde
        pygame.draw.polygon(self.image, COR_FOLHA,
                            [(15, 8), (9, 2), (12, 6), (15, 4), (18, 6), (21, 2)])

    def aplicar(self, jogador):
        jogador.ativar_turbo(POWERUP_DURACAO_TURBO)


class BananaDourada(PowerUp):
    """Duas bananas cruzadas: dois projéteis lado a lado.

    Dá tiro duplo (dois projéteis lado a lado) por um tempo."""

    def _desenhar(self):
        b1 = _pequena_banana()
        b2 = _pequena_banana()
        r1 = pygame.transform.rotozoom(b1, -30, 1)
        r2 = pygame.transform.rotozoom(b2, 30, 1)
        self.image.blit(r1, (9 - r1.get_width() // 2,
                             13 - r1.get_height() // 2))
        self.image.blit(r2, (21 - r2.get_width() // 2,
                             19 - r2.get_height() // 2))

    def _efeito_dinamico(self, alvo, fase):
        # pulso dourado atrás das bananas
        raio = 13 + int(math.sin(fase * 0.12) * 2)
        anel = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(anel, (255, 210, 70, 60), (15, 15), raio)
        anel.set_alpha(int(40 + 40 * (0.5 + 0.5 * math.sin(fase * 0.1))))
        alvo.blit(anel, (0, 0))

    def aplicar(self, jogador):
        jogador.ativar_tiro_duplo(POWERUP_DURACAO_TIRO_DUPLO)


class CascaBanana(PowerUp):
    """Fatia de melancia: a casca protege, exatamente como o escudo.

    Cria um escudo que bloqueia todo o dano por um tempo."""

    def _desenhar(self):
        # fatia de melancia
        pygame.draw.ellipse(self.image, COR_MELANCIA_CASCA_ESC, (4, 3, 22, 21), 4)
        pygame.draw.ellipse(self.image, (240, 242, 200), (6, 5, 18, 18), 2)
        pygame.draw.ellipse(self.image, COR_MELANCIA_POLPA, (8, 6, 14, 15))
        # brilho na polpa
        pygame.draw.arc(self.image, (255, 200, 205), (9, 7, 10, 8), 0.0, math.pi, 2)
        # sementes pretas
        for sx, sy in ((11, 11), (15, 12), (13, 16), (18, 15)):
            pygame.draw.circle(self.image, (44, 32, 44), (sx, sy), 1)

    def aplicar(self, jogador):
        jogador.ativar_escudo(POWERUP_DURACAO_ESCUDO)


class BananaExplosiva(PowerUp):
    """Abacaxi explosivo: corpo 'armado' com pontas e textura.

    Mega tiro: projéteis mais fortes por um tempo."""

    def _desenhar(self):
        # corpo do abacaxi (elipse com textura de losangos)
        pygame.draw.ellipse(self.image, COR_ABACAXI, (8, 10, 14, 13))
        pygame.draw.ellipse(self.image, COR_ABACAXI_ESC, (8, 10, 14, 13), 1)
        for dy in (-2, 2):
            pygame.draw.line(self.image, COR_ABACAXI_ESC,
                             (12, 12 + dy), (19, 21 + dy), 1)
            pygame.draw.line(self.image, COR_ABACAXI_ESC,
                             (20, 12 + dy), (13, 21 + dy), 1)
        # coroa de folhas pontudas
        pygame.draw.polygon(self.image, COR_FOLHA,
                            [(15, 10), (9, 4), (13, 9), (15, 5), (17, 9), (21, 4)])
        pygame.draw.circle(self.image, (220, 200, 120), (12, 14), 2)
        pygame.draw.circle(self.image, (255, 220, 130), (21, 16), 1)

    def _efeito_dinamico(self, alvo, fase):
        # pulso laranja (sensação de carga/prestes a explodir)
        raio = 12 + int(math.sin(fase * 0.16) * 2)
        anel = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(anel, (255, 150, 40, 55), (15, 15), raio)
        anel.set_alpha(int(35 + 35 * (0.5 + 0.5 * math.sin(fase * 0.2))))
        alvo.blit(anel, (0, 0))

    def aplicar(self, jogador):
        jogador.ativar_mega_tiro(POWERUP_DURACAO_MEGA_TIRO)


class BananaCoracao(PowerUp):
    """Maçã em forma de coração: fruta que recupera a vida.

    Recupera 1 vida (efeito instantâneo)."""

    def _desenhar(self):
        # coração-fruta
        pygame.draw.circle(self.image, COR_MACA, (11, 11), 6)
        pygame.draw.circle(self.image, COR_MACA, (19, 11), 6)
        pygame.draw.polygon(self.image, COR_MACA,
                            [(6, 13), (24, 13), (15, 23)])
        pygame.draw.circle(self.image, COR_MACA_ESC, (11, 11), 6, 1)
        pygame.draw.circle(self.image, COR_MACA_ESC, (19, 11), 6, 1)
        pygame.draw.polygon(self.image, COR_MACA_ESC, [(6, 13), (24, 13), (15, 23)], 1)
        # cabinho + folhinha
        pygame.draw.line(self.image, (96, 66, 38), (15, 5), (15, 10), 2)
        pygame.draw.polygon(self.image, COR_FOLHA,
                            [(14, 6), (22, 1), (21, 7), (15, 9)])
        # brilho
        pygame.draw.circle(self.image, (255, 225, 235), (9, 9), 2)

    def aplicar(self, jogador):
        jogador.recuperar_vida()


class BananaEstrela(PowerUp):
    """Banana dourada premiada: brilhos, aura e sensação de recompensa.

    Concede pontos bônus (efeito instantâneo)."""

    def _desenhar(self):
        # aura suave dourada
        pygame.draw.circle(self.image, (255, 220, 90, 55), (15, 15), 12)
        # banana maior inclinada
        b = _pequena_banana(cor=(255, 210, 50), ponta=(150, 106, 30))
        b = pygame.transform.rotozoom(b, -20, 1.25)
        self.image.blit(b, (15 - b.get_width() // 2,
                            15 - b.get_height() // 2))
        # estrelinhas nos cantos
        cor_brilho = (255, 255, 190)
        for sx, sy in ((6, 5), (25, 9), (4, 23), (24, 24)):
            pygame.draw.line(self.image, cor_brilho, (sx - 2, sy), (sx + 2, sy), 1)
            pygame.draw.line(self.image, cor_brilho, (sx, sy - 2), (sx, sy + 2), 1)

    def _efeito_dinamico(self, alvo, fase):
        # cintilação: estrelinha acesa de tempos em tempos em cantos
        if fase % 7 == 0:
            pos = [(5, 5), (25, 5), (5, 25), (25, 25)][int(fase // 7) % 4]
            pygame.draw.line(alvo, (255, 255, 200), (pos[0] - 3, pos[1]),
                             (pos[0] + 3, pos[1]), 1)
            pygame.draw.line(alvo, (255, 255, 200), (pos[0], pos[1] - 3),
                             (pos[0], pos[1] + 3), 1)

    def aplicar(self, jogador):
        return POWERUP_BONUS_PONTOS