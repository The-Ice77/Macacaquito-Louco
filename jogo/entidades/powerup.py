"""
Classes de power-ups: itens coletáveis que dão vantagens ao jogador.

Cada power-up cai do topo da tela devagar, é coletado ao tocar o jogador
e desaparece se sair da tela.
"""
import pygame

from .entidade import Entidade
from ..settings import (
    ALTURA, POWERUP_VELOCIDADE,
    COR_POWERUP_TURBO, COR_POWERUP_DOURADO, COR_POWERUP_CASCA,
    COR_POWERUP_EXPLOSIVA, COR_POWERUP_CORACAO, COR_POWERUP_ESTRELA,
    COR_POWERUP_SIMBOLO,
    POWERUP_DURACAO_TURBO, POWERUP_DURACAO_TIRO_DUPLO,
    POWERUP_DURACAO_ESCUDO, POWERUP_DURACAO_MEGA_TIRO,
    POWERUP_BONUS_PONTOS,
)


class PowerUp(Entidade):
    """Base comum: círculo colorido com um símbolo identificador."""

    def __init__(self, x, y):
        super().__init__(x, y, POWERUP_VELOCIDADE)
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self._desenhar()

    def _desenhar(self):
        # sobrescrito por cada tipo
        pass

    def aplicar(self, jogador):
        """Aplica o efeito. Retorna pontos extras quando houver."""
        return None

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA:
            self.kill()


class BananaTurbo(PowerUp):
    """Aumenta temporariamente a velocidade do jogador."""

    def _desenhar(self):
        pygame.draw.circle(self.image, COR_POWERUP_TURBO, (15, 15), 15)
        for x, y, larg in ((9, 7, 12), (7, 13, 16), (9, 19, 12)):
            pygame.draw.rect(self.image, COR_POWERUP_SIMBOLO,
                             (x, y, larg, 3))

    def aplicar(self, jogador):
        jogador.ativar_turbo(POWERUP_DURACAO_TURBO)


class BananaDourada(PowerUp):
    """Dá tiro duplo (dois projéteis lado a lado) por um tempo."""

    def _desenhar(self):
        pygame.draw.circle(self.image, COR_POWERUP_DOURADO, (15, 15), 15)
        pygame.draw.rect(self.image, COR_POWERUP_SIMBOLO, (8, 8, 6, 14))
        pygame.draw.rect(self.image, COR_POWERUP_SIMBOLO, (16, 8, 6, 14))

    def aplicar(self, jogador):
        jogador.ativar_tiro_duplo(POWERUP_DURACAO_TIRO_DUPLO)


class CascaBanana(PowerUp):
    """Cria um escudo que bloqueia todo o dano por um tempo."""

    def _desenhar(self):
        pygame.draw.circle(self.image, COR_POWERUP_CASCA, (15, 15), 15)
        pygame.draw.circle(self.image, (255, 255, 255), (15, 15), 12, 4)

    def aplicar(self, jogador):
        jogador.ativar_escudo(POWERUP_DURACAO_ESCUDO)


class BananaExplosiva(PowerUp):
    """Mega tiro: projéteis mais fortes por um tempo."""

    def _desenhar(self):
        pygame.draw.circle(self.image, COR_POWERUP_EXPLOSIVA, (15, 15), 15)
        for ponto in ((15, 4), (26, 15), (15, 26), (4, 15)):
            pygame.draw.line(self.image, COR_POWERUP_SIMBOLO,
                             ponto, (15, 15), 2)

    def aplicar(self, jogador):
        jogador.ativar_mega_tiro(POWERUP_DURACAO_MEGA_TIRO)


class BananaCoracao(PowerUp):
    """Recupera 1 vida (efeito instantâneo)."""

    def _desenhar(self):
        pygame.draw.circle(self.image, COR_POWERUP_CORACAO, (15, 15), 15)
        pygame.draw.circle(self.image, (120, 20, 60), (10, 11), 5)
        pygame.draw.circle(self.image, (120, 20, 60), (20, 11), 5)
        pygame.draw.polygon(self.image, (120, 20, 60),
                            [(5, 13), (25, 13), (15, 24)])

    def aplicar(self, jogador):
        jogador.recuperar_vida()


class BananaEstrela(PowerUp):
    """Concede pontos bônus (efeito instantâneo)."""

    def _desenhar(self):
        pygame.draw.circle(self.image, COR_POWERUP_ESTRELA, (15, 15), 15)
        pygame.draw.polygon(self.image, COR_POWERUP_SIMBOLO,
                            [(15, 3), (25, 15), (15, 27), (5, 15)])

    def aplicar(self, jogador):
        return POWERUP_BONUS_PONTOS