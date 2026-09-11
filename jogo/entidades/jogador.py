"""
Classe do Jogador: controla movimento, vida e efeitos temporários.

O protagonista é um macaco pilotando um avião feito de banana. O desenho é
feito por frame com formas do Pygame, permitindo pequenas animações:
inclinação em voo, hélice girando, chama de propulsão e reações do macaco.
A hitbox permanece em um retângulo simples (40x40) fixo.
"""
import math

import pygame

from .entidade import Entidade
from ..settings import LARGURA, ALTURA, COR_JOGADOR, POWERUP_MULT_TURBO
from ..visual.tema import banana_surface
from ..sons import tocar

# Paleta do avião-banana
_CASCA = (250, 225, 70)
_CASCA_ESC = (190, 165, 45)
_ASAS = (120, 200, 92)
_PELE = (255, 220, 180)


def _desenhar_aviao(superficie, reacao="normal"):
    """Desenha o avião-banana (com o macaco) em uma superfície 40x40.

    `reacao` muda a expressão do macaco: normal, feliz, dano, surpresa,
    comemorar.
    """
    # cauda / leme traseiro
    pygame.draw.polygon(superficie, _CASCA,
                        [(16, 36), (19, 29), (23, 36)])
    pygame.draw.polygon(superficie, _CASCA_ESC,
                        [(21, 29), (23, 36), (25, 35)])

    # asas (folhas verdes) com inclinação sutil
    pygame.draw.polygon(superficie, _ASAS,
                        [(5, 25), (14, 28), (14, 33), (5, 32)])
    pygame.draw.polygon(superficie, _ASAS,
                        [(35, 25), (26, 28), (26, 33), (35, 32)])
    pygame.draw.line(superficie, (70, 130, 60),
                     (5, 25), (14, 28), 1)
    pygame.draw.line(superficie, (70, 130, 60),
                     (35, 25), (26, 28), 1)

    # fuselagem: banana curvada (o corpo do avião)
    banana = pygame.transform.rotozoom(banana_surface(13), -90, 1)
    superficie.blit(banana, (20 - banana.get_width() // 2,
                             21 - banana.get_height() // 2))

    # macaco pilotando (cabeça no topo da fuselagem)
    cs, cy = 20, 15
    pygame.draw.circle(superficie, COR_JOGADOR, (cs - 7, cy - 3), 5)
    pygame.draw.circle(superficie, COR_JOGADOR, (cs + 7, cy - 3), 5)
    pygame.draw.circle(superficie, _PELE, (cs - 7, cy - 3), 2)
    pygame.draw.circle(superficie, _PELE, (cs + 7, cy - 3), 2)
    pygame.draw.circle(superficie, COR_JOGADOR, (cs, cy), 10)
    pygame.draw.ellipse(superficie, _PELE, (cs - 6, cy - 3, 12, 11))

    # olhos conforme a reação
    cor_olho = (60, 40, 20)
    if reacao == "dano":
        for ex in (-4, 4):
            pygame.draw.line(superficie, cor_olho,
                             (cs + ex - 2, cy - 1), (cs + ex + 2, cy + 2), 2)
            pygame.draw.line(superficie, cor_olho,
                             (cs + ex - 2, cy + 2), (cs + ex + 2, cy - 1), 2)
    elif reacao == "surpresa":
        for ex in (-4, 4):
            pygame.draw.circle(superficie, (255, 255, 255),
                               (cs + ex, cy), 3)
            pygame.draw.circle(superficie, cor_olho, (cs + ex, cy), 1)
    else:
        for ex in (-4, 4):
            pygame.draw.circle(superficie, cor_olho, (cs + ex, cy), 2)

    # boca conforme a reação
    if reacao in ("feliz", "comemorar"):
        pygame.draw.arc(superficie, (120, 50, 25),
                        (cs - 5, cy + 3, 10, 9), 0.2, math.pi - 0.2, 2)
    elif reacao == "dano":
        pygame.draw.arc(superficie, (120, 50, 25),
                        (cs - 3, cy + 3, 6, 5), math.pi, math.tau, 2)
    elif reacao == "surpresa":
        pygame.draw.circle(superficie, (120, 50, 25), (cs, cy + 5), 2)
    else:
        pygame.draw.arc(superficie, (120, 50, 25),
                        (cs - 3, cy + 3, 6, 5), 0.2, math.pi - 0.2, 2)

    # braços: levantados ao comemorar
    if reacao == "comemorar":
        pygame.draw.line(superficie, COR_JOGADOR,
                         (cs - 6, cy + 4), (cs - 11, cy - 4), 3)
        pygame.draw.line(superficie, COR_JOGADOR,
                         (cs + 6, cy + 4), (cs + 11, cy - 4), 3)


def _desenhar_helice(superficie, angulo):
    """Hélice girando no nariz (topo) do avião."""
    cx, cy = 20, 4
    pygame.draw.circle(superficie, (90, 90, 100), (cx, cy), 3)
    for i in (0, 1):
        a = angulo * 0.6 + i * math.pi / 2
        dx = math.cos(a) * 8
        dy = math.sin(a) * 2.5
        pygame.draw.ellipse(superficie, (220, 230, 240),
                            (cx + dx - 5, cy + dy - 1.5, 10, 3))


def _desenhar_chama(superficie, timer):
    """Chama de propulsão na parte traseira (embaixo)."""
    flick = int(math.sin(timer * 0.9) * 1.5)
    pygame.draw.polygon(superficie, (255, 190, 60),
                        [(21, 36), (19, 39 + flick), (20, 37), (22, 36)])
    pygame.draw.polygon(superficie, (255, 255, 140),
                        [(21, 36), (20, 37), (21, 37)])


class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        # imagem transparente; a hitbox (rect) continua 40x40
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.base_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        _desenhar_aviao(self.base_image, "normal")

        self.tilt_atual = 0.0
        self.bob_timer = 0
        self.prop_angulo = 0
        self.timer = 0

        # reações contextuais (curtas)
        self.reacao = "normal"
        self.reacao_timer = 0

        self.vida = 5
        self.vida_max = 5

        self.velocidade_base = self.velocidade
        self.velocidade_atual = self.velocidade

        # Timers dos efeitos temporários (em frames, 60 = 1s)
        self.timer_turbo = 0
        self.timer_tiro_duplo = 0
        self.timer_mega_tiro = 0
        self.timer_escudo = 0

    def reagir(self, nome, frames=28):
        """Dispara uma reação visual curta (feliz, dano, surpresa...)."""
        self.reacao = nome
        self.reacao_timer = max(self.reacao_timer, frames)

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
        """Inclina, balança e anima o avião (sem mexer na hitbox)."""
        alvo = direcao_x * 8
        self.tilt_atual += (alvo - self.tilt_atual) * 0.25
        if abs(self.tilt_atual) < 0.5:
            self.tilt_atual = 0.0

        if movendo:
            self.bob_timer += 1
        else:
            self.bob_timer = 0
        # balanço de voo (contínuo) + balanço de movimento
        osc = int(math.sin(self.timer * 0.2) * 1)
        bob = (int(math.sin(self.bob_timer * 0.35) * 2) if movendo else 0)

        if self.reacao_timer > 0:
            self.reacao_timer -= 1
            if self.reacao_timer == 0:
                self.reacao = "normal"

        # velocidade da hélice maior com turbo/movimento
        passo = 30 if (movendo or self.timer_turbo > 0) else 16
        self.prop_angulo = (self.prop_angulo + passo) % 360

        base = pygame.Surface((40, 40), pygame.SRCALPHA)
        _desenhar_aviao(base, self.reacao)
        _desenhar_helice(base, self.prop_angulo)
        _desenhar_chama(base, self.timer)
        if self.timer_turbo > 0:
            _desenhar_chama(base, self.timer + 4)

        if abs(self.tilt_atual) >= 0.5:
            rot = pygame.transform.rotozoom(base, -self.tilt_atual, 1)
        else:
            rot = base
        nova = pygame.Surface((40, 40), pygame.SRCALPHA)
        nova.blit(rot, (20 - rot.get_width() // 2,
                        20 - rot.get_height() // 2 + osc + bob))
        self.image = nova

    def update(self):
        self._aplicar_tremor()
        self.timer += 1

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
            if not self.timer_escudo:
                tocar("escudo_expirado")

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