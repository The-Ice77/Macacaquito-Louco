"""
Classes de projéteis: tiro (jogador e inimigos) e explosão.

O Tiro é uma base simples e reutilizável: move-se por um vetor de velocidade
(vx, vy), pode miram levemente um alvo (homing) e pode gerar uma explosão
ao atingir o jogador ou ao sair da área útil.
"""
import math

import pygame

from .entidade import Entidade, escalar, redimensionar
from ..settings import (
    ALTURA, LARGURA, MARGEM_SAIDA_PROJETIL,
    FATOR_ESCALA_PROJETIL, FATOR_ESCALA_EXPLOSAO,
    COR_BANANA, COR_BANANA_POLPA, COR_PROJETIL_INIMIGO,
)
from ..visual.tema import banana_surface
from ..sons import tocar


def _escurecer(cor, fator=0.6):
    return tuple(max(0, min(255, int(c * fator))) for c in cor)


def _aclarar(cor, fator=1.3):
    return tuple(max(0, min(255, int(c * fator) + 12)) for c in cor)


def direcao_para(ox, oy, ax, ay):
    """Retorna vetor unitário (dx, dy) apontando de (ox, oy) até (ax, ay)."""
    dx = ax - ox
    dy = ay - oy
    tamanho = math.hypot(dx, dy)
    if tamanho == 0:
        return 0, 1
    return dx / tamanho, dy / tamanho


def _desenhar_banana(lado, cor):
    """Banana descascada (só a polpa), ponto de partida da estética do jogo.

    Reaproveita a silhueta crescente já usada nos menus e a recolore como
    polpa clara, com a polpa visível nas extremidades e textura em miniatura.
    """
    superficie = pygame.Surface((lado, lado), pygame.SRCALPHA)
    t_casca = max(2, lado // 3 - 1)
    ban = banana_surface(t_casca, cor=cor)
    # reduz para caber dentro do quadro do projétil (mantendo proporção)
    larg, alt = ban.get_size()
    escala = min(lado / larg, lado / alt)
    ban = redimensionar(ban, int(larg * escala), int(alt * escala))
    b_x = (lado - ban.get_width()) // 2
    b_y = (lado - ban.get_height()) // 2
    superficie.blit(ban, (b_x, b_y))

    # polpa: veia central + sementinhas para leitura de "fruta descascada"
    ponta = _escurecer(_aclarar(cor, 0.6), 0.7)
    cx = lado // 2
    for y in (0, 1):
        pygame.draw.line(superficie, _escurecer(cor, 0.82),
                         (cx - 2 + y, lado // 2 - 2 + y * 2),
                         (cx - 2 + y, lado // 2 + 3 + y * 2), 1)
    for dx, dy in ((-4, -3), (4, -1)):
        pygame.draw.circle(superficie, ponta, (cx + dx, lado // 2 + dy), 1)
    # leve rastro translúcido abaixo (sensação de subida)
    pygame.draw.rect(superficie, (255, 255, 255, 70),
                     (lado // 2 - 1, lado - 3, 2, 2))
    return superficie


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
        # amplia o projétil para acompanhar as naves maiores (hitbox proporcional)
        centro = self.rect.center
        self.image = escalar(self.image, FATOR_ESCALA_PROJETIL)
        self.rect = self.image.get_rect(center=centro)

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
        # som conforme o tamanho da explosão (raio do projétil)
        if self.raio_explosao <= 35:
            tocar("explosao_missil")
            tocar("explosao_missil_aguda")
        elif self.raio_explosao <= 60:
            tocar("explosao_bomba")
        else:
            tocar("explosao_grande")
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
    """Projétil do jogador: banana descascada, sempre para cima, sem explosão.

    Só muda a representação visual; velocidade, hitbox, dano e colisão são
    os mesmos do Tiro base.
    """

    def __init__(self, x, y, cor=COR_BANANA, tamanho=12, dano=1, brilho=False):
        super().__init__(x, y, 0, -10, cor=cor, tamanho=tamanho)
        self.dano = dano
        if cor is None:
            cor = COR_BANANA
        # a imagem vira a banana descascada (rect/hitbox continua igual)
        cor_polpa = COR_BANANA_POLPA if cor == COR_BANANA else cor
        self.image = _desenhar_banana(tamanho, cor_polpa)
        self.rect = self.image.get_rect(center=self.rect.center)
        # amplia a banana para acompanhar a nave maior
        centro = self.rect.center
        self.image = escalar(self.image, FATOR_ESCALA_PROJETIL)
        self.rect = self.image.get_rect(center=centro)


class Explosao(Entidade):
    """Explosão visual com dano de área aplicado uma única vez.

    Animação: o círculo cresce rápido, ganha círculos menores ao redor,
    depois encolhe com fade e é removido do jogo.
    """

    def __init__(self, x, y, raio, cor=None, alvo=None):
        super().__init__(x, y, 0)
        self.raio_dano = max(2, raio)          # raio de dano (gameplay)
        self.raio_max = max(2, int(raio * FATOR_ESCALA_EXPLOSAO))  # visual
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
        if math.hypot(dx, dy) <= self.raio_dano:
            return 1
        return 0

    def update(self):
        self.timer += 1
        if self.timer >= self.duracao:
            self.kill()
            return
        self._desenhar_estado()
