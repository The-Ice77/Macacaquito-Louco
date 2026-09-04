"""
Classes de inimigos: forças policiais que perseguem o protagonista.

Usa classe abstrata para garantir o método de movimentação em cada inimigo.
"""
from abc import ABC, abstractmethod
import math
import random

import pygame

from .entidade import Entidade
from .settings import (
    LARGURA, ALTURA,
    COR_GUARDA, COR_HELICOPTERO, COR_VIATURA,
    COR_GUARDAPESADO, COR_CHEFE, COR_CHEFE_FASE2,
    VIDA_GUARDA, PONTOS_GUARDA, VELOCIDADE_GUARDA,
    VIDA_HELICOPTERO, PONTOS_HELICOPTERO, VELOCIDADE_HELICOPTERO,
    VIDA_VIATURA, PONTOS_VIATURA, VELOCIDADE_VIATURA,
    VIDA_GUARDAPESADO, PONTOS_GUARDAPESADO, VELOCIDADE_GUARDAPESADO,
    VIDA_CHEFE, PONTOS_CHEFE, VELOCIDADE_CHEFE,
    VEL_BALA, VEL_BALA_TAMANHO, COR_BALA,
    VEL_MISSIL, VEL_MISSIL_TAMANHO, COR_MISSIL,
    PERSECUCAO_HELICOPTERO, RAIO_EXPLOSAO_MISSIL, COR_EXPLOSAO_MISSIL,
    VEL_RAJADA, VEL_RAJADA_TAMANHO, COR_RAJADA,
    QTD_RAJADA_VIATURA, INTERVALO_RAJADA, FREQ_RAJADA_VIATURA,
    VEL_BOMBA, VEL_BOMBA_TAMANHO, COR_BOMBA,
    RAIO_EXPLOSAO_BOMBA, COR_EXPLOSAO_BOMBA, INTERVALO_BOMBA,
    VEL_MISSIL_BOSS, VEL_MISSIL_BOSS_TAMANHO, COR_MISSIL_BOSS,
    PERSECUCAO_BOSS, RAIO_EXPLOSAO_MISSIL_BOSS, COR_EXPLOSAO_MISSIL_BOSS,
    INTERVALO_TIRO_BOSS_FASE1,
    VEL_LEQUE, VEL_LEQUE_TAMANHO, COR_LEQUE, QTD_LEQUE_BOSS,
    INTERVALO_LEQUE_BOSS,
    VEL_BOMBA_BOSS, VEL_BOMBA_BOSS_TAMANHO, COR_BOMBA_BOSS,
    RAIO_EXPLOSAO_BOMBA_BOSS, COR_EXPLOSAO_BOMBA_BOSS,
    INTERVALO_BOMBA_BOSS,
    LINHA_EXPLOSAO_BOMBA,
)
from .tiro import Tiro, direcao_para


class Inimigo(Entidade, ABC):
    """Classe base abstrata de todos os inimigos."""

    def __init__(self, x, y, velocidade, vida, pontos, cor, tamanho=40):
        super().__init__(x, y, velocidade)
        self.image = pygame.Surface((tamanho, tamanho))
        self.rect = self.image.get_rect(center=(x, y))
        self.vida = vida
        self.pontos = pontos
        self.cor = cor
        self.tiros_inimigos = None
        self.explosoes = None
        self.todos_sprites = None
        self._desenhar()

    @abstractmethod
    def _movimentar(self):
        """Define o movimento específico do inimigo."""

    @abstractmethod
    def _desenhar(self):
        """Desenha a forma geométrica do inimigo."""

    def tomar_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.kill()

    def saiu_da_tela(self):
        margem = 80
        if (self.rect.top > ALTURA + margem or
                self.rect.bottom < -margem or
                self.rect.right < -margem or
                self.rect.left > LARGURA + margem):
            self.kill()

    def _registrar_tiro(self, tiro):
        """Adiciona um projétil aos grupos corretos para desenho e colisão."""
        if self.tiros_inimigos is not None:
            self.tiros_inimigos.add(tiro)
        if self.todos_sprites is not None:
            self.todos_sprites.add(tiro)

    def update(self):
        self._movimentar()
        self.saiu_da_tela()


class Guarda(Inimigo):
    """Inimigo básico que desce e dispara uma bala simples."""

    def __init__(self, x, y, referencia_jogador):
        super().__init__(x, y, VELOCIDADE_GUARDA, VIDA_GUARDA,
                         PONTOS_GUARDA, COR_GUARDA)
        self.jogador = referencia_jogador
        self.timer_tiro = 0
        self.intervalo_tiro = 60

    def _movimentar(self):
        self.rect.y += self.velocidade
        if self.jogador is not None:
            if self.rect.centerx < self.jogador.rect.centerx:
                self.rect.x += 1
            elif self.rect.centerx > self.jogador.rect.centerx:
                self.rect.x -= 1

    def _desenhar(self):
        self.image.fill(self.cor)
        pygame.draw.circle(self.image, (0, 0, 0), (20, 20), 10, 2)
        pygame.draw.rect(self.image, (255, 255, 255),
                         (14, 2, 12, 8))

    def atirar(self):
        # bala simples: pequena, rápida, reta para baixo
        tiro = Tiro(self.rect.centerx, self.rect.bottom,
                    0, VEL_BALA, cor=COR_BALA, tamanho=VEL_BALA_TAMANHO)
        self._registrar_tiro(tiro)

    def update(self):
        self._movimentar()
        self.saiu_da_tela()
        self.timer_tiro += 1
        if self.timer_tiro >= self.intervalo_tiro:
            self.atirar()
            self.timer_tiro = 0


class HelicopteroPolicial(Inimigo):
    """Inimigo intermediário que dispara um míssil mirado no jogador."""

    def __init__(self, x, y, referencia_jogador):
        super().__init__(x, y, VELOCIDADE_HELICOPTERO, VIDA_HELICOPTERO,
                         PONTOS_HELICOPTERO, COR_HELICOPTERO, tamanho=50)
        self.jogador = referencia_jogador
        self.timer_tiro = 0
        self.intervalo_tiro = 100

    def _movimentar(self):
        self.rect.y += self.velocidade
        if self.jogador is not None:
            if self.rect.centerx < self.jogador.rect.centerx:
                self.rect.x += 2
            elif self.rect.centerx > self.jogador.rect.centerx:
                self.rect.x -= 2
        self.rect.x = max(0, min(self.rect.x, LARGURA - 50))

    def _desenhar(self):
        self.image.fill(self.cor)
        pygame.draw.rect(self.image, (0, 0, 0), (5, 20, 40, 10))
        pygame.draw.rect(self.image, (220, 220, 220), (10, 2, 30, 4))

    def atirar(self):
        # míssil mirado na posição atual do jogador, com leve correção
        if self.jogador is None:
            return
        dx, dy = direcao_para(
            self.rect.centerx, self.rect.bottom,
            self.jogador.rect.centerx, self.jogador.rect.centery,
        )
        tiro = Tiro(
            self.rect.centerx, self.rect.bottom,
            dx * VEL_MISSIL, dy * VEL_MISSIL,
            cor=COR_MISSIL, tamanho=VEL_MISSIL_TAMANHO,
            homing=self.jogador, velo_perseguicao=PERSECUCAO_HELICOPTERO,
            raio_explosao=RAIO_EXPLOSAO_MISSIL,
            cor_explosao=COR_EXPLOSAO_MISSIL,
        )
        tiro.todos_sprites = self.todos_sprites
        tiro.explosoes = self.explosoes
        self._registrar_tiro(tiro)

    def update(self):
        self._movimentar()
        self.saiu_da_tela()
        self.timer_tiro += 1
        if self.timer_tiro >= self.intervalo_tiro:
            self.atirar()
            self.timer_tiro = 0


class ViaturaRapida(Inimigo):
    """Inimigo veloz que atravessa a tela e dispara uma rajada de balas."""

    def __init__(self, x, y, direcao):
        super().__init__(x, y, VELOCIDADE_VIATURA, VIDA_VIATURA,
                         PONTOS_VIATURA, COR_VIATURA, tamanho=35)
        self.velocidade_x = direcao * VELOCIDADE_VIATURA
        self.timer_rajada = 0
        self.tiros_rajada = 0
        self.intervalo_rajada = 50

    def _movimentar(self):
        self.rect.x += self.velocidade_x
        self.rect.y += 1

    def _desenhar(self):
        self.image.fill(self.cor)
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 35, 5))
        pygame.draw.rect(self.image, (255, 255, 255), (0, 30, 35, 5))

    def _disparar_bala(self):
        tiro = Tiro(self.rect.centerx, self.rect.bottom,
                    0, VEL_RAJADA, cor=COR_RAJADA,
                    tamanho=VEL_RAJADA_TAMANHO)
        self._registrar_tiro(tiro)

    def _iniciar_rajada(self):
        self.tiros_rajada = QTD_RAJADA_VIATURA

    def update(self):
        self._movimentar()
        self.saiu_da_tela()
        self.timer_rajada += 1
        if self.tiros_rajada > 0:
            if self.timer_rajada >= INTERVALO_RAJADA:
                self._disparar_bala()
                self.tiros_rajada -= 1
                self.timer_rajada = 0
        elif self.timer_rajada >= self.intervalo_rajada:
            self._iniciar_rajada()
            self.timer_rajada = 0


class GuardaPesado(Inimigo):
    """Inimigo raro e lento que dispara uma bomba explosiva grande."""

    def __init__(self, x, y, referencia_jogador):
        super().__init__(x, y, VELOCIDADE_GUARDAPESADO, VIDA_GUARDAPESADO,
                         PONTOS_GUARDAPESADO, COR_GUARDAPESADO, tamanho=50)
        self.jogador = referencia_jogador
        self.timer_tiro = 0
        self.intervalo_tiro = INTERVALO_BOMBA

    def _movimentar(self):
        self.rect.y += self.velocidade
        if self.jogador is not None:
            if self.rect.centerx < self.jogador.rect.centerx:
                self.rect.x += 1
            elif self.rect.centerx > self.jogador.rect.centerx:
                self.rect.x -= 1

    def _desenhar(self):
        self.image.fill(self.cor)
        pygame.draw.circle(self.image, (0, 0, 0), (25, 25), 14, 2)
        pygame.draw.rect(self.image, (255, 255, 255), (10, 2, 30, 12))

    def atirar(self):
        # bomba lenta, grande, explode ao tocar o jogador ou na base
        tiro = Tiro(self.rect.centerx, self.rect.bottom,
                    0, VEL_BOMBA, cor=COR_BOMBA,
                    tamanho=VEL_BOMBA_TAMANHO,
                    homing=self.jogador,
                    raio_explosao=RAIO_EXPLOSAO_BOMBA,
                    cor_explosao=COR_EXPLOSAO_BOMBA,
                    explodir_na_linha=LINHA_EXPLOSAO_BOMBA)
        tiro.todos_sprites = self.todos_sprites
        tiro.explosoes = self.explosoes
        self._registrar_tiro(tiro)

    def update(self):
        self._movimentar()
        self.saiu_da_tela()
        self.timer_tiro += 1
        if self.timer_tiro >= self.intervalo_tiro:
            self.atirar()
            self.timer_tiro = 0


class ChefeFinal(Inimigo):
    """Chefe final: ruivo, fica no topo, com padrões e fase 2."""

    def __init__(self, x, referencia_jogador):
        self.esta_na_fase2 = False
        super().__init__(x, 70, VELOCIDADE_CHEFE, VIDA_CHEFE,
                         PONTOS_CHEFE, COR_CHEFE, tamanho=70)
        self.jogador = referencia_jogador
        self.direcao = 1
        self.timer_tiro = 0
        self.intervalo_tiro = INTERVALO_TIRO_BOSS_FASE1
        self.grupo_inimigos = None
        self.metade_vida = VIDA_CHEFE / 2
        # timers dos padrões específicos da fase 2
        self.timer_leque = 0
        self.intervalo_leque = INTERVALO_LEQUE_BOSS
        self.timer_bomba = 0
        self.intervalo_bomba = INTERVALO_BOMBA_BOSS
        self.timer_chamada = 0

    def _movimentar(self):
        self.rect.x += self.direcao * self.velocidade
        if self.rect.x <= 20 or self.rect.x >= LARGURA - 70:
            self.direcao *= -1

    def _desenhar(self):
        cor = COR_CHEFE_FASE2 if self.esta_na_fase2 else self.cor
        self.image.fill(cor)
        pygame.draw.circle(self.image, (0, 0, 0), (35, 40), 16, 2)
        pygame.draw.rect(self.image, (120, 40, 20), (25, 8, 20, 10))

    def entrar_fase2(self):
        if not self.esta_na_fase2:
            self.esta_na_fase2 = True
            self.velocidade = self.velocidade + 2
            self.intervalo_tiro = 35
            self._desenhar()

    def _novo_tiro(self, tiro):
        tiro.todos_sprites = self.todos_sprites
        tiro.explosoes = self.explosoes
        self._registrar_tiro(tiro)

    def _atacar_fase1(self):
        # tiro direcionado no jogador (míssil especial, leve correção)
        if self.jogador is None:
            return
        dx, dy = direcao_para(
            self.rect.centerx, self.rect.bottom,
            self.jogador.rect.centerx, self.jogador.rect.centery,
        )
        tiro = Tiro(
            self.rect.centerx, self.rect.bottom,
            dx * VEL_MISSIL_BOSS, dy * VEL_MISSIL_BOSS,
            cor=COR_MISSIL_BOSS, tamanho=VEL_MISSIL_BOSS_TAMANHO,
            homing=self.jogador, velo_perseguicao=PERSECUCAO_BOSS,
            raio_explosao=RAIO_EXPLOSAO_MISSIL_BOSS,
            cor_explosao=COR_EXPLOSAO_MISSIL_BOSS,
        )
        self._novo_tiro(tiro)

    def _leque(self):
        # 5 projéteis em ângulos diferentes, sem perseguição
        inicio = -2 if QTD_LEQUE_BOSS % 2 == 0 else -(QTD_LEQUE_BOSS // 2)
        for i in range(QTD_LEQUE_BOSS):
            angulo = math.radians(inicio + i)
            vx = math.sin(angulo) * VEL_LEQUE
            vy = math.cos(angulo) * VEL_LEQUE
            tiro = Tiro(self.rect.centerx, self.rect.bottom,
                        vx, vy, cor=COR_LEQUE,
                        tamanho=VEL_LEQUE_TAMANHO)
            self._novo_tiro(tiro)

    def _bomba_especial(self):
        tiro = Tiro(self.rect.centerx, self.rect.bottom,
                    0, VEL_BOMBA_BOSS, cor=COR_BOMBA_BOSS,
                    tamanho=VEL_BOMBA_BOSS_TAMANHO,
                    homing=self.jogador,
                    raio_explosao=RAIO_EXPLOSAO_BOMBA_BOSS,
                    cor_explosao=COR_EXPLOSAO_BOMBA_BOSS,
                    explodir_na_linha=LINHA_EXPLOSAO_BOMBA)
        self._novo_tiro(tiro)

    def chamar_guardas(self):
        if self.grupo_inimigos is None:
            return
        for _ in range(2):
            guarda = Guarda(
                random.randint(40, LARGURA - 40), -40, self.jogador
            )
            self.grupo_inimigos.add(guarda)

    def update(self):
        self._movimentar()

        if not self.esta_na_fase2 and self.vida <= self.metade_vida:
            self.entrar_fase2()

        self.timer_tiro += 1
        if self.timer_tiro >= self.intervalo_tiro:
            self._atacar_fase1()
            self.timer_tiro = 0

        if self.esta_na_fase2:
            # leque
            self.timer_leque += 1
            if self.timer_leque >= self.intervalo_leque:
                self._leque()
                self.timer_leque = 0
            # bomba especial
            self.timer_bomba += 1
            if self.timer_bomba >= self.intervalo_bomba:
                self._bomba_especial()
                self.timer_bomba = 0
            # convocação de inimigos menores
            self.timer_chamada += 1
            if self.timer_chamada >= 300:
                self.chamar_guardas()
                self.timer_chamada = 0
