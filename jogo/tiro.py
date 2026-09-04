"""
Classes de projéteis: tiro (jogador e inimigos) e explosão.

O Tiro é uma base simples e reutilizável: move-se por um vetor de velocidade
(vx, vy), pode miram levemente um alvo (homing) e pode gerar uma explosão
ao atingir o jogador ou ao sair da área útil.
"""
import math

import pygame

from .entidade import Entidade
from .settings import (
    ALTURA, LARGURA, MARGEM_SAIDA_PROJETIL,
    COR_BANANA, COR_PROJETIL_INIMIGO,
)


def direcao_para(ox, oy, ax, ay):
    """Retorna vetor unitário (dx, dy) apontando de (ox, oy) até (ax, ay)."""
    dx = ax - ox
    dy = ay - oy
    tamanho = math.hypot(dx, dy)
    if tamanho == 0:
        return 0, 1
    return dx / tamanho, dy / tamanho


class Tiro(Entidade):
    """Projétil com movimento vetorial e comportamento configurável."""

    def __init__(self, x, y, vx, vy, cor=None, tamanho=10,
                 homing=None, velo_perseguicao=0, raio_explosao=0,
                 cor_explosao=None, explodir_na_linha=None):
        super().__init__(x, y, 0)
        self.image = pygame.Surface((tamanho, tamanho))
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx
        self.vy = vy
        self.homing = homing
        self.velo_perseguicao = velo_perseguicao
        self.raio_explosao = raio_explosao
        self.explosoes = None
        self.todos_sprites = None
        self.cor_explosao = cor_explosao
        self.explodir_na_linha = explodir_na_linha

        if cor is None:
            cor = COR_BANANA
        self._desenhar(cor)

    def _desenhar(self, cor):
        self.image.fill(cor)
        pygame.draw.rect(self.image, (0, 0, 0),
                         (0, 0, self.image.get_width(), self.image.get_height()),
                         1)

    def _corrigir_trajetoria(self):
        """Corrige levemente a direção em direção ao alvo (homing suave)."""
        alvo = self.homing
        if alvo is None or alvo.rect is None:
            return
        dx, dy = direcao_para(
            self.rect.centerx, self.rect.centery,
            alvo.rect.centerx, alvo.rect.centery,
        )
        velocidade = math.hypot(self.vx, self.vy)
        self.vx += (dx * velocidade - self.vx) * self.velo_perseguicao
        self.vy += (dy * velocidade - self.vy) * self.velo_perseguicao

    def saiu_da_tela(self):
        return (self.rect.right < -MARGEM_SAIDA_PROJETIL or
                self.rect.left > LARGURA + MARGEM_SAIDA_PROJETIL or
                self.rect.top > ALTURA + MARGEM_SAIDA_PROJETIL or
                self.rect.bottom < -MARGEM_SAIDA_PROJETIL)

    def criar_explosao(self, x, y):
        """Cria uma explosão na posição dada e remove o projétil."""
        explosao = Explosao(x, y, self.raio_explosao,
                            cor=self.cor_explosao,
                            alvo=self.homing)
        if self.explosoes is not None:
            self.explosoes.add(explosao)
        if self.todos_sprites is not None:
            self.todos_sprites.add(explosao)
        self.kill()

    def explodir(self):
        """Cria a explosão (se houver) na posição atual."""
        if self.raio_explosao <= 0:
            return
        self.criar_explosao(self.rect.centerx, self.rect.centery)

    def update(self):
        self._corrigir_trajetoria()
        self.rect.x += self.vx
        self.rect.y += self.vy
        if (self.explodir_na_linha is not None
                and self.rect.top >= self.explodir_na_linha):
            self.explodir()
        elif self.saiu_da_tela():
            self.explodir()


class TiroJogador(Tiro):
    """Projétil do jogador (banana), sempre para cima, sem explosão."""

    def __init__(self, x, y):
        super().__init__(x, y, 0, -10, cor=COR_BANANA, tamanho=12)


class Explosao(Entidade):
    """Explosão visual com dano de área aplicado uma única vez."""

    def __init__(self, x, y, raio, cor=None, alvo=None):
        super().__init__(x, y, 0)
        self.raio = max(2, raio)
        self.alvo = alvo
        self.dano_aplicado = False
        self.timer = 0
        self.duracao = 12
        if cor is None:
            cor = COR_PROJETIL_INIMIGO
        self.cor = cor
        self.image = pygame.Surface((self.raio * 2, self.raio * 2),
                                    pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self._desenhar(1)

    def _desenhar(self, raio):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, self.cor, (raio, raio), raio)
        pygame.draw.circle(self.image, (255, 255, 255), (raio, raio),
                           max(1, raio // 2))

    def aplicar_dano_se_no_alcance(self):
        """Aplica 1 dano ao alvo uma única vez, se dentro do raio."""
        if self.dano_aplicado or self.alvo is None:
            return 0
        self.dano_aplicado = True
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        if math.hypot(dx, dy) <= self.raio:
            return 1
        return 0

    def update(self):
        self.timer += 1
        escala = 1 - (self.timer / self.duracao)
        if escala <= 0:
            self.kill()
            return
        novo_raio = max(1, int(self.raio * escala))
        self.image = pygame.Surface((self.raio * 2, self.raio * 2),
                                    pygame.SRCALPHA)
        centro = self.raio
        self._desenhar_em(centro, novo_raio)

    def _desenhar_em(self, centro, raio):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, self.cor, (centro, centro), raio)
        pygame.draw.circle(self.image, (255, 255, 255),
                           (centro, centro), max(1, raio // 2))
