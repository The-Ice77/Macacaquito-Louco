"""
Classe base para todos os objetos do jogo (jogador, tiros, robôs).
"""
import pygame


def escalar(superficie, fator):
    """Redimensiona a superfície mantendo a proporção (desenho + arte)."""
    largura = max(1, int(superficie.get_width() * fator))
    altura = max(1, int(superficie.get_height() * fator))
    return pygame.transform.smoothscale(superficie, (largura, altura))


def redimensionar(superficie, largura, altura):
    """Redimensiona a superfície para um tamanho exato."""
    largura = max(1, int(largura))
    altura = max(1, int(altura))
    return pygame.transform.smoothscale(superficie, (largura, altura))


class Entidade(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade):
        super().__init__()
        self.velocidade = velocidade
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.tremor_timer = 0

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def ativar_tremor(self, frames=8):
        """Faz a entidade tremer ao levar dano."""
        self.tremor_timer = frames

    def _aplicar_tremor(self):
        """Oscila o rect durante o tempo de tremor (chamado no update)."""
        if self.tremor_timer <= 0:
            return
        self.tremor_timer -= 1
        # ciclo simétrico para não deslocar a posição permanentemente
        fase = self.tremor_timer % 4
        if fase == 0:
            self.rect.x += 2
        elif fase == 1:
            self.rect.y -= 1
        elif fase == 2:
            self.rect.x -= 2
        else:
            self.rect.y += 1
