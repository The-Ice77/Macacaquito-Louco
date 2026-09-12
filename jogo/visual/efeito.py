"""
Efeitos visuais geométricos simples: partículas, flashes e fragmentos.

Apenas formas do Pygame, sem imagens. Os efeitos são registrados nos grupos
de sprites e se removem sozinhos quando o timer acaba.
"""
import math
import random

import pygame

from ..entidades.entidade import Entidade


class EfeitoVisual(Entidade):
    """Base dos efeitos: sem dano, com timer de duração."""

    def __init__(self, x, y, tamanho=8):
        super().__init__(x, y, 0)
        self.image = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 0

    def _expirou(self, duracao):
        self.timer += 1
        return self.timer >= duracao


class Particula(EfeitoVisual):
    """Pequeno fragmento com velocidade, gravidade e fade opcional."""

    def __init__(self, x, y, vx, vy, cor, tamanho=4, duracao=20,
                 gravidade=0.1, formato="quadrado", linha=None):
        lado = max(tamanho * 2 + 2, (linha or tamanho) + 2)
        super().__init__(x, y, lado)
        self.vx = vx
        self.vy = vy
        self.cor = cor
        self.gravidade = gravidade
        self.duracao = duracao
        self.formato = formato
        self.linha = linha
        self._desenhar(tamanho)

    def _desenhar(self, tamanho):
        self.image.fill((0, 0, 0, 0))
        if self.linha is not None:
            altura = self.image.get_height()
            pygame.draw.rect(self.image, self.cor,
                             (1, altura // 2 - tamanho // 2, self.linha, tamanho))
        elif self.formato == "circulo":
            pygame.draw.circle(self.image, self.cor,
                               (tamanho + 1, tamanho + 1), tamanho)
        else:
            pygame.draw.rect(self.image, self.cor,
                             (1, 1, tamanho * 2, max(2, tamanho * 2 - 2)))

    def update(self):
        if self._expirou(self.duracao):
            self.kill()
            return
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vy += self.gravidade
        resto = 1 - self.timer / self.duracao
        self.image.set_alpha(int(255 * resto))


class Flash(EfeitoVisual):
    """Flash circular de impacto: cresce e encolhe rapidamente."""

    def __init__(self, x, y, cor, raio_max=12, duracao=8):
        super().__init__(x, y, raio_max * 2 + 2)
        self.cor = cor
        self.raio_max = raio_max
        self.duracao = duracao
        self.centro = raio_max + 1

    def update(self):
        if self._expirou(self.duracao):
            self.kill()
            return
        progresso = self.timer / self.duracao
        fator = 1 - abs(progresso - 0.5) * 2     # sobe até o meio e desce
        raio = max(1, int(self.raio_max * fator) + 1)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, self.cor, (self.centro, self.centro), raio)
        pygame.draw.circle(self.image, (255, 255, 255),
                           (self.centro, self.centro), max(1, raio // 2))
        self.image.set_alpha(int(255 * (1 - progresso * 0.7)))


def criar_fragmentos(x, y, cor, grupo_sprites, grupo_efeitos, qtd=8):
    """Estilhaços que se afastam do ponto de destruição do inimigo."""
    for _ in range(qtd):
        angulo = random.uniform(0, math.tau)
        vel = random.uniform(1, 4)
        particula = Particula(
            x, y,
            math.cos(angulo) * vel, math.sin(angulo) * vel - 1,
            cor, tamanho=random.randint(2, 4),
            duracao=random.randint(10, 18), gravidade=0.06,
        )
        grupo_sprites.add(particula)
        grupo_efeitos.add(particula)


def criar_flash_impacto(x, y, grupo_sprites, grupo_efeitos,
                        cor=(255, 240, 150), raio_max=12):
    """Flash breve quando um tiro acerta (mas não destrói) um inimigo."""
    flash = Flash(x, y, cor, raio_max=raio_max, duracao=8)
    grupo_sprites.add(flash)
    grupo_efeitos.add(flash)


def criar_flash_forte(x, y, grupo_sprites, grupo_efeitos):
    """Flash de impacto maior e mais evidente (chefe)."""
    flash = Flash(x, y, (255, 200, 80), raio_max=26, duracao=12)
    grupo_sprites.add(flash)
    grupo_efeitos.add(flash)


def criar_particulas_propulsao(x, y, grupo_sprites, grupo_efeitos, turbo=False):
    """Partícula de propulsão que arrasta atrás do avião."""
    if turbo:
        cor = random.choice([(255, 240, 120), (255, 200, 80), (255, 255, 255)])
        tamanho = random.randint(2, 4)
        duracao = random.randint(12, 20)
    else:
        cor = random.choice([(255, 210, 100), (255, 180, 70)])
        tamanho = 2
        duracao = random.randint(10, 16)
    particula = Particula(
        x + random.randint(-4, 4), y + random.randint(0, 6),
        random.uniform(-0.15, 0.15), random.uniform(1.2, 2.4),
        cor, tamanho=tamanho, duracao=duracao, gravidade=0,
        formato="circulo",
    )
    grupo_sprites.add(particula)
    grupo_efeitos.add(particula)


def criar_particulas_coleta(x, y, cor, grupo_sprites, grupo_efeitos):
    """Partículas que sobem ao redor do jogador ao coletar um power-up."""
    for _ in range(10):
        angulo = random.uniform(math.pi, math.tau)
        vel = random.uniform(1, 3)
        particula = Particula(
            x + random.randint(-10, 10), y + random.randint(-10, 10),
            math.cos(angulo) * vel, math.sin(angulo) * vel,
            cor if random.random() < 0.7 else (255, 255, 255),
            tamanho=3, duracao=24, gravidade=-0.02, formato="circulo",
        )
        grupo_sprites.add(particula)
        grupo_efeitos.add(particula)


def criar_linha_turbo(x, y, grupo_sprites, grupo_efeitos):
    """Linha de velocidade atrás do jogador enquanto o turbo está ativo."""
    particula = Particula(
        x + random.randint(-18, 18), y + random.randint(0, 8),
        random.uniform(-0.3, 0.3), random.uniform(0.8, 1.6),
        (255, 240, 120), tamanho=2, duracao=12, gravidade=0,
        linha=random.randint(12, 22),
    )
    grupo_sprites.add(particula)
    grupo_efeitos.add(particula)


def criar_explosao_destruicao(x, y, cor, grupo_sprites, grupo_efeitos):
    """Flash maior + estilhaços para a destruição completa de um inimigo."""
    flash = Flash(x, y, cor, raio_max=20, duracao=12)
    grupo_sprites.add(flash)
    grupo_efeitos.add(flash)
    criar_fragmentos(x, y, cor, grupo_sprites, grupo_efeitos, qtd=12)