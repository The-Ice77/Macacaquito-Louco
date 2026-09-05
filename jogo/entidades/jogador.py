"""
Classe do Jogador: controla movimento, vida e efeitos temporários.
"""
import math

import pygame

from .entidade import Entidade
from ..settings import LARGURA, ALTURA, COR_JOGADOR, POWERUP_MULT_TURBO


class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        self.image.fill(COR_JOGADOR)
        pygame.draw.circle(self.image, (255, 220, 180), (20, 20), 8)

        # base para as animações visuais (inclinação e balanço)
        self.base_image = self.image.copy()
        self.tilt_atual = 0.0
        self.bob_timer = 0

        self.vida = 5
        self.vida_max = 5

        self.velocidade_base = self.velocidade
        self.velocidade_atual = self.velocidade

        # Timers dos efeitos temporários (em frames, 60 = 1s)
        self.timer_turbo = 0
        self.timer_tiro_duplo = 0
        self.timer_mega_tiro = 0
        self.timer_escudo = 0

    def ativar_turbo(self, frames):
        self.timer_turbo = max(self.timer_turbo, frames)
        self.velocidade_atual = self.velocidade_base * POWERUP_MULT_TURBO

    def ativar_tiro_duplo(self, frames):
        self.timer_tiro_duplo = max(self.timer_tiro_duplo, frames)

    def ativar_mega_tiro(self, frames):
        self.timer_mega_tiro = max(self.timer_mega_tiro, frames)

    def ativar_escudo(self, frames):
        self.timer_escudo = max(self.timer_escudo, frames)

    def escudo_ativo(self):
        return self.timer_escudo > 0

    def recuperar_vida(self):
        """Recupera 1 vida e retorna True se houver espaço para curar."""
        if self.vida >= self.vida_max:
            return False
        self.vida += 1
        return True

    def efeitos_ativos(self):
        """Lista com os nomes dos efeitos ativos (para o HUD)."""
        efeitos = []
        if self.timer_turbo > 0:
            efeitos.append("TURBO")
        if self.timer_tiro_duplo > 0:
            efeitos.append("2X")
        if self.timer_mega_tiro > 0:
            efeitos.append("MEGA")
        if self.timer_escudo > 0:
            efeitos.append("ESCUDO")
        return efeitos

    def _atualizar_visual(self, direcao_x, movendo):
        """Inclina e balança o avião visualmente, sem mexer na hitbox."""
        alvo = direcao_x * 8
        self.tilt_atual += (alvo - self.tilt_atual) * 0.25
        if abs(self.tilt_atual) < 0.5:
            self.tilt_atual = 0.0
        if movendo:
            self.bob_timer += 1
        else:
            self.bob_timer = 0
        bob = int(math.sin(self.bob_timer * 0.35) * 2) if movendo else 0

        if abs(self.tilt_atual) >= 0.5:
            base = pygame.transform.rotozoom(self.base_image,
                                             -self.tilt_atual, 1)
        else:
            base = self.base_image
        nova = pygame.Surface((40, 40), pygame.SRCALPHA)
        nova.blit(base, (20 - base.get_width() // 2,
                         20 - base.get_height() // 2 + bob))
        self.image = nova

    def update(self):
        self._aplicar_tremor()

        if self.timer_turbo > 0:
            self.timer_turbo -= 1
            if self.timer_turbo == 0:
                self.velocidade_atual = self.velocidade_base
        if self.timer_tiro_duplo > 0:
            self.timer_tiro_duplo -= 1
        if self.timer_mega_tiro > 0:
            self.timer_mega_tiro -= 1
        if self.timer_escudo > 0:
            self.timer_escudo -= 1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.mover(0, -self.velocidade_atual)
        if keys[pygame.K_s]:
            self.mover(0, self.velocidade_atual)
        if keys[pygame.K_a]:
            self.mover(-self.velocidade_atual, 0)
        if keys[pygame.K_d]:
            self.mover(self.velocidade_atual, 0)

        # limites de tela
        self.rect.x = max(0, min(self.rect.x, LARGURA - 40))
        self.rect.y = max(0, min(self.rect.y, ALTURA - 40))

        direcao_x = 0
        if keys[pygame.K_d]:
            direcao_x = 1
        elif keys[pygame.K_a]:
            direcao_x = -1
        movendo = (keys[pygame.K_w] or keys[pygame.K_s] or
                   keys[pygame.K_a] or keys[pygame.K_d])
        self._atualizar_visual(direcao_x, movendo)