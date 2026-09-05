"""
Classes de projéteis: tiro (jogador e inimigos) e explosão.

O Tiro é uma base simples e reutilizável: move-se por um vetor de velocidade
(vx, vy), pode miram levemente um alvo (homing) e pode gerar uma explosão
ao atingir o jogador ou ao sair da área útil.
"""
import math

import pygame

from .entidade import Entidade
from ..settings import (
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

    def __init__(self, x, y, cor=COR_BANANA, tamanho=12, dano=1, brilho=False):
        super().__init__(x, y, 0, -10, cor=cor, tamanho=tamanho)
        self.dano = dano
        if cor is None:
            cor = COR_BANANA
        # cor mais clara para o rastro atrás do projétil
        clara = tuple(min(255, c + 70) for c in cor)
        pygame.draw.rect(self.image, clara,
                         (tamanho // 2 - 1, tamanho // 2, 2, tamanho // 2))
        if brilho:
            # brilho ao redor do tiro (indicador do tiro duplo)
            pygame.draw.rect(self.image, (255, 255, 255),
                             (1, 1, tamanho - 2, tamanho - 2), 2)


class Explosao(Entidade):
    """Explosão visual com dano de área aplicado uma única vez.

    Animação: o círculo cresce rápido, ganha círculos menores ao redor,
    depois encolhe com fade e é removido do jogo.
    """

    def __init__(self, x, y, raio, cor=None, alvo=None):
        super().__init__(x, y, 0)
        self.raio_max = max(2, raio)
        self.alvo = alvo
        self.dano_aplicado = False
        self.timer = 0
        self.duracao = 20
        if cor is None:
            cor = COR_PROJETIL_INIMIGO
        self.cor = cor
        # superfície grande o suficiente para abrigar o círculo e os satélites
        banda = self.raio_max + self.raio_max // 4 + 4
        lado = banda * 2
        self.centro = lado // 2
        self.image = pygame.Surface((lado, lado), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self._desenhar_estado()

    def _raio_atual(self):
        """Cresce até 35% da duração e encolhe no restante."""
        progresso = self.timer / self.duracao
        if progresso < 0.35:
            fator = progresso / 0.35
        else:
            fator = 1 - (progresso - 0.35) / 0.65
        return max(1, int(self.raio_max * fator) + 1)

    def _desenhar_estado(self):
        raio = self._raio_atual()
        alpha = int(255 * (0.6 + 0.4 * (1 - self.timer / self.duracao)))
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, self.cor,
                           (self.centro, self.centro), raio + 2)
        pygame.draw.circle(self.image, (255, 255, 255),
                           (self.centro, self.centro), max(1, raio // 2))
        # círculos menores ao redor da borda da explosão
        for angulo in (0, math.pi / 2, math.pi, math.pi * 3 / 2):
            dx = math.cos(angulo) * (raio + 3)
            dy = math.sin(angulo) * (raio + 3)
            pygame.draw.circle(
                self.image, (255, 200, 80),
                (int(self.centro + dx), int(self.centro + dy)),
                max(1, raio // 4 + 1))
        self.image.set_alpha(alpha)

    def aplicar_dano_se_no_alcance(self):
        """Aplica 1 dano ao alvo uma única vez, se dentro do raio."""
        if self.dano_aplicado or self.alvo is None:
            return 0
        self.dano_aplicado = True
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        if math.hypot(dx, dy) <= self.raio_max:
            return 1
        return 0

    def update(self):
        self.timer += 1
        if self.timer >= self.duracao:
            self.kill()
            return
        self._desenhar_estado()
