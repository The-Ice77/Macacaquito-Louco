"""
Classes de inimigos: forças policiais que perseguem o protagonista.

Usa classe abstrata para garantir o método de movimentação em cada inimigo.
"""
from abc import ABC, abstractmethod
import random

import pygame

from .entidade import Entidade
from .settings import (
    LARGURA, ALTURA,
    COR_GUARDA, COR_HELICOPTERO, COR_VIATURA, COR_PROJETIL_INIMIGO,
    COR_GUARDAPESADO, COR_CHEFE, COR_CHEFE_FASE2, COR_PROJETIL_FORTE,
    VIDA_GUARDA, PONTOS_GUARDA, VELOCIDADE_GUARDA,
    VIDA_HELICOPTERO, PONTOS_HELICOPTERO, VELOCIDADE_HELICOPTERO,
    VIDA_VIATURA, PONTOS_VIATURA, VELOCIDADE_VIATURA,
    VIDA_GUARDAPESADO, PONTOS_GUARDAPESADO, VELOCIDADE_GUARDAPESADO,
    VIDA_CHEFE, PONTOS_CHEFE, VELOCIDADE_CHEFE,
)


def criar_tiro_inimigo(x, y, cor=None):
    """Cria um projétil que desce (disparado por inimigos)."""
    from .tiro import Tiro
    try:
        return Tiro(x, y, direcao=-1, cor=cor)
    except Exception:
        return None


class Inimigo(Entidade, ABC):
    """Classe base abstrata de todos os inimigos."""

    def __init__(self, x, y, velocidade, vida, pontos, cor, tamanho=40):
        super().__init__(x, y, velocidade)
        self.image = pygame.Surface((tamanho, tamanho))
        self.rect = self.image.get_rect(center=(x, y))
        self.vida = vida
        self.pontos = pontos
        self.cor = cor
        self._desenhar()
        self.tiros_inimigos = None

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

    def update(self):
        self._movimentar()
        self.saiu_da_tela()


class Guarda(Inimigo):
    """Inimigo básico que desce em direção ao jogador e dispara."""

    def __init__(self, x, y, referencia_jogador):
        super().__init__(x, y, VELOCIDADE_GUARDA, VIDA_GUARDA,
                         PONTOS_GUARDA, COR_GUARDA)
        self.jogador = referencia_jogador
        self.timer_tiro = 0
        self.intervalo_tiro = 70

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
        if self.tiros_inimigos is None:
            return
        tiro = criar_tiro_inimigo(self.rect.centerx, self.rect.bottom)
        if tiro:
            self.tiros_inimigos.add(tiro)

    def update(self):
        self._movimentar()
        self.saiu_da_tela()
        self.timer_tiro += 1
        if self.timer_tiro >= self.intervalo_tiro:
            self.atirar()
            self.timer_tiro = 0


class HelicopteroPolicial(Inimigo):
    """Inimigo intermediário que acompanha o X do jogador e dispara."""

    def __init__(self, x, y, referencia_jogador):
        super().__init__(x, y, VELOCIDADE_HELICOPTERO, VIDA_HELICOPTERO,
                         PONTOS_HELICOPTERO, COR_HELICOPTERO, tamanho=50)
        self.jogador = referencia_jogador
        self.timer_tiro = 0
        self.intervalo_tiro = 50

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
        if self.tiros_inimigos is None:
            return None
        tiro = criar_tiro_inimigo(self.rect.centerx, self.rect.bottom)
        if tiro:
            self.tiros_inimigos.add(tiro)
        return tiro

    def update(self):
        self._movimentar()
        self.saiu_da_tela()
        self.timer_tiro += 1
        if self.timer_tiro >= self.intervalo_tiro:
            self.atirar()
            self.timer_tiro = 0


class ViaturaRapida(Inimigo):
    """Inimigo veloz que atravessa a tela rapidamente pelas laterais."""

    def __init__(self, x, y, direcao):
        super().__init__(x, y, VELOCIDADE_VIATURA, VIDA_VIATURA,
                         PONTOS_VIATURA, COR_VIATURA, tamanho=35)
        self.velocidade_x = direcao * VELOCIDADE_VIATURA

    def _movimentar(self):
        self.rect.x += self.velocidade_x
        self.rect.y += 1

    def _desenhar(self):
        self.image.fill(self.cor)
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 35, 5))
        pygame.draw.rect(self.image, (255, 255, 255), (0, 30, 35, 5))


class GuardaPesado(Inimigo):
    """Inimigo raro, lento e resistente, com ataque mais forte."""

    def __init__(self, x, y, referencia_jogador):
        super().__init__(x, y, VELOCIDADE_GUARDAPESADO, VIDA_GUARDAPESADO,
                         PONTOS_GUARDAPESADO, COR_GUARDAPESADO, tamanho=50)
        self.jogador = referencia_jogador
        self.timer_tiro = 0
        self.intervalo_tiro = 90

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
        if self.tiros_inimigos is None:
            return
        tiro = criar_tiro_inimigo(
            self.rect.centerx, self.rect.bottom, COR_PROJETIL_FORTE
        )
        if tiro:
            self.tiros_inimigos.add(tiro)

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
        self.intervalo_tiro = 40
        self.timer_chamada = 0
        self.intervalo_chamada = 150
        self.grupo_inimigos = None
        self.metade_vida = VIDA_CHEFE / 2

    def _movimentar(self):
        self.rect.x += self.direcao * self.velocidade
        if self.rect.x <= 20 or self.rect.x >= LARGURA - 70:
            self.direcao *= -1

    def _desenhar(self):
        cor = COR_CHEFE_FASE2 if self.esta_na_fase2 else self.cor
        self.image.fill(cor)
        # corpo ruivo (círculo central)
        pygame.draw.circle(self.image, (0, 0, 0), (35, 40), 16, 2)
        # "cabelos" ruivos e charme cartunesco
        pygame.draw.rect(self.image, (120, 40, 20), (25, 8, 20, 10))

    def entrar_fase2(self):
        if not self.esta_na_fase2:
            self.esta_na_fase2 = True
            self.velocidade = self.velocidade + 2
            self.intervalo_tiro = 25
            self._desenhar()

    def atirar(self):
        if self.tiros_inimigos is None:
            return
        x = self.rect.centerx
        y = self.rect.bottom
        if self.esta_na_fase2:
            # barragem de projéteis fortes em paralelo na fase 2
            for dx in (-30, 0, 30):
                tiro = criar_tiro_inimigo(x + dx, y, COR_PROJETIL_FORTE)
                if tiro:
                    self.tiros_inimigos.add(tiro)
        else:
            for dx in (-15, 15):
                tiro = criar_tiro_inimigo(x + dx, y)
                if tiro:
                    self.tiros_inimigos.add(tiro)

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
            self.atirar()
            self.timer_tiro = 0

        # fase 2: chama inimigos menores periodicamente
        if self.esta_na_fase2:
            self.timer_chamada += 1
            if self.timer_chamada >= self.intervalo_chamada:
                self.chamar_guardas()
                self.timer_chamada = 0

