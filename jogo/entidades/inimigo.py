"""
Classes de inimigos: forças policiais que perseguem o protagonista.

Usa classe abstrata para garantir o método de movimentação em cada inimigo.
"""
from abc import ABC, abstractmethod
import math
import random

import pygame

from .entidade import Entidade, escalar, redimensionar
from ..settings import (
    LARGURA, ALTURA,
    COR_GUARDA, COR_HELICOPTERO, COR_VIATURA,
    COR_GUARDAPESADO, COR_CHEFE, COR_CHEFE_FASE2,
    FATOR_ESCALA_INIMIGO,
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
from ..sons import tocar
from ..visual.efeito import Flash, Particula


def _escurecer(cor, fator=0.7):
    """Versão mais escura de uma cor (para contornos e sombras)."""
    return tuple(max(0, int(c * fator)) for c in cor)


def _aclarar(cor, fator=0.5):
    """Versão mais clara de uma cor (mistura com branco)."""
    return tuple(int(c + (255 - c) * fator) for c in cor)


def _sombra_oval(superficie, x, y, larg, alt, alpha=70):
    """Desenha uma sombra suave (elipse translúcida) sobre a superfície."""
    sombra = pygame.Surface((larg, alt), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, alpha), (0, 0, larg, alt))
    superficie.blit(sombra, (x, y))


class Inimigo(Entidade, ABC):
    """Classe base abstrata de todos os inimigos."""

    def __init__(self, x, y, velocidade, vida, pontos, cor, tamanho=40):
        super().__init__(x, y, velocidade)
        self.image = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.vida = vida
        self.pontos = pontos
        self.cor = cor
        self.tiros_inimigos = None
        self.explosoes = None
        self.todos_sprites = None
        self._desenhar()
        # aplica a escala visual (e redimensiona a hitbox de forma proporcional)
        self.image = escalar(self.image, FATOR_ESCALA_INIMIGO)
        self.rect = self.image.get_rect(center=(x, y))
        # imagens e estados para a inclinação visual (sem mexer na hitbox)
        self.base_image = self.image.copy()
        self.tilt_atual = 0.0
        self.inclinacao_max = 6
        self.ultimo_x = x
        self.timer = 0

    @abstractmethod
    def _movimentar(self):
        """Define o movimento específico do inimigo."""

    @abstractmethod
    def _desenhar(self):
        """Desenha a forma geométrica do inimigo."""

    def tomar_dano(self, dano):
        self.vida -= dano
        self.ativar_tremor()
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

    def _atualizar_visual(self):
        """Inclina o desenho conforme o movimento horizontal (só visual)."""
        self.timer += 1
        dx = self.rect.x - self.ultimo_x
        self.ultimo_x = self.rect.x
        if dx > 0:
            alvo = self.inclinacao_max
        elif dx < 0:
            alvo = -self.inclinacao_max
        else:
            alvo = 0.0
        self.tilt_atual += (alvo - self.tilt_atual) * 0.25
        if abs(self.tilt_atual) < 0.5:
            self.tilt_atual = 0.0
            self.image = self.base_image
        else:
            self.image = pygame.transform.rotozoom(
                self.base_image, -self.tilt_atual, 1)

    def update(self):
        self._movimentar()
        self._atualizar_visual()
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
        # pequena oscilação horizontal (dá "vida" ao guarda)
        self.rect.x += math.sin(self.timer * 0.08) * 0.5
        if self.jogador is not None:
            if self.rect.centerx < self.jogador.rect.centerx:
                self.rect.x += 1
            elif self.rect.centerx > self.jogador.rect.centerx:
                self.rect.x -= 1

    def _desenhar(self):
        """Viatura policial vista de cima: frente virada para baixo."""
        s = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.image = s
        _sombra_oval(s, 5, 31, 30, 6)

        # rodas (pequenas e escuras, aparecendo nas laterais)
        for x in (5, 31):
            pygame.draw.rect(s, (25, 25, 32), (x, 13, 4, 7), border_radius=2)
            pygame.draw.rect(s, (25, 25, 32), (x, 23, 4, 7), border_radius=2)

        # contorno + corpo arredondado
        pygame.draw.rect(s, (14, 44, 110), (7, 7, 26, 28), border_radius=7)
        pygame.draw.rect(s, self.cor, (8, 8, 24, 26), border_radius=6)

        # cabine (teto) com contorno
        pygame.draw.rect(s, _aclarar(self.cor, 0.5), (13, 10, 14, 12),
                         border_radius=3)
        pygame.draw.rect(s, (10, 30, 90), (13, 10, 14, 12), 1,
                         border_radius=3)

        # vidros traseiro e dianteiro
        pygame.draw.rect(s, (16, 50, 130), (14, 12, 12, 4), border_radius=2)
        pygame.draw.rect(s, (175, 220, 250), (14, 20, 12, 5), border_radius=2)

        # barra de luzes rotativas no teto
        pygame.draw.rect(s, (25, 30, 60), (15, 16, 10, 4), border_radius=2)
        pygame.draw.circle(s, (255, 70, 70), (17, 18), 2)
        pygame.draw.circle(s, (80, 130, 255), (23, 18), 2)

        # capô (frente) e faróis dianteiros
        pygame.draw.rect(s, _aclarar(self.cor, 0.25), (11, 26, 18, 4),
                         border_radius=2)
        pygame.draw.rect(s, (255, 250, 210), (10, 31, 3, 2))
        pygame.draw.rect(s, (255, 250, 210), (27, 31, 3, 2))

        # contorno lateral leve (dá volume)
        pygame.draw.line(s, (16, 50, 130), (9, 15), (9, 29), 2)
        pygame.draw.line(s, (16, 50, 130), (31, 15), (31, 29), 2)

    def atirar(self):
        # bala simples: pequena, rápida, reta para baixo
        tiro = Tiro(self.rect.centerx, self.rect.bottom,
                    0, VEL_BALA, cor=COR_BALA, tamanho=VEL_BALA_TAMANHO)
        self._registrar_tiro(tiro)
        tocar("tiro_guarda")

    def update(self):
        self._movimentar()
        self._atualizar_visual()
        self.saiu_da_tela()
        self._aplicar_tremor()
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
        self.inclinacao_max = 8
        self.rotor_angulo = 0

    def _movimentar(self):
        self.rect.y += self.velocidade
        if self.jogador is not None:
            if self.rect.centerx < self.jogador.rect.centerx:
                self.rect.x += 2
            elif self.rect.centerx > self.jogador.rect.centerx:
                self.rect.x -= 2
        self.rect.x = max(0, min(self.rect.x, LARGURA - self.rect.width))

    def _desenhar(self):
        """Helicóptero policial visto de cima: frente virada para baixo."""
        s = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image = s
        _sombra_oval(s, 9, 40, 32, 8)

        # boom da cauda (parte traseira, topo) com estabilizadores
        pygame.draw.rect(s, (55, 65, 78), (21, 4, 8, 18), border_radius=3)
        pygame.draw.rect(s, (35, 42, 52), (21, 4, 8, 18), 1, border_radius=3)
        pygame.draw.polygon(s, (45, 55, 66),
                            [(21, 4), (16, 1), (22, 2)])
        pygame.draw.polygon(s, (45, 55, 66),
                            [(29, 4), (34, 1), (28, 2)])
        pygame.draw.circle(s, (70, 80, 90), (25, 4), 2)  # rotor de cauda

        # fuselagem principal com contorno
        pygame.draw.rect(s, _escurecer(self.cor, 0.7), (9, 20, 32, 22),
                         border_radius=8)
        pygame.draw.rect(s, self.cor, (10, 21, 30, 20), border_radius=7)

        # painéis laterais
        pygame.draw.line(s, (30, 60, 120), (12, 26), (12, 38), 2)
        pygame.draw.line(s, (30, 60, 120), (38, 26), (38, 38), 2)

        # para-brisa dianteiro (frente ao jogador)
        pygame.draw.rect(s, (180, 225, 255), (16, 34, 18, 6), border_radius=3)

        # nariz arredondado
        pygame.draw.ellipse(s, _escurecer(self.cor, 0.85), (17, 39, 16, 6))

        # patins (esquis) de pouso
        pygame.draw.line(s, (120, 130, 145), (11, 41), (9, 45), 3)
        pygame.draw.line(s, (120, 130, 145), (39, 41), (41, 45), 3)
        pygame.draw.line(s, (90, 100, 115), (4, 46), (46, 46), 3)

        # conteúdos laterais (pods de carga/motor)
        pygame.draw.rect(s, (90, 100, 115), (5, 24, 4, 12), border_radius=2)
        pygame.draw.rect(s, (90, 100, 115), (41, 24, 4, 12), border_radius=2)

        # mastro central da hélice (o rotor é desenhado em cima)
        pygame.draw.circle(s, (70, 80, 90), (25, 23), 4)

    def _desenhar_rotor(self):
        """Hélice do topo, girando no centro do corpo (semi-transparente).

        O rotor é desenhado na escala original e depois redimensionado para
        acompanhar o tamanho (e a inclinação) da imagem atual.
        """
        cx, cy = 25, 23
        laminas = pygame.Surface((48, 14), pygame.SRCALPHA)
        pygame.draw.ellipse(laminas, (215, 225, 235, 170), (0, 5, 48, 4))
        laminas = pygame.transform.rotozoom(laminas, self.rotor_angulo, 1)

        overlay = pygame.Surface((50, 50), pygame.SRCALPHA)
        overlay.blit(laminas,
                     (cx - laminas.get_width() // 2,
                      cy - laminas.get_height() // 2))
        pygame.draw.circle(overlay, (85, 95, 110), (cx, cy), 4)

        overlay = redimensionar(overlay, *self.image.get_size())
        self.image.blit(overlay, (0, 0))

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
        tocar("tiro_helicoptero")

    def update(self):
        self._movimentar()
        self._atualizar_visual()
        self.saiu_da_tela()
        self._aplicar_tremor()
        self.rotor_angulo = (self.rotor_angulo + 26) % 360
        self._desenhar_rotor()
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
        self.inclinacao_max = 10
        self._virado = False

    def _movimentar(self):
        self.rect.x += self.velocidade_x
        # leve balanço vertical enquanto avança (sensação de velocidade)
        self.rect.y += 1 + math.sin(self.timer * 0.12) * 0.5

    def _desenhar(self):
        """Aeronave de persecução alongada, com o bico apontando para a direita."""
        s = pygame.Surface((35, 35), pygame.SRCALPHA)
        self.image = s

        # rastro curto de velocidade atrás (esquerda)
        for x, y in ((4, 13), (2, 18), (5, 23)):
            pygame.draw.line(s, (150, 190, 255), (1, y), (x, y), 1)

        # asas delta (superior e inferior)
        pygame.draw.polygon(s, _escurecer(self.cor, 0.75),
                            [(10, 13), (17, 5), (20, 5), (15, 14)])
        pygame.draw.polygon(s, _escurecer(self.cor, 0.75),
                            [(10, 22), (17, 30), (20, 30), (15, 21)])

        # contorno + corpo alongado
        pygame.draw.rect(s, (6, 20, 70), (6, 12, 26, 11), border_radius=5)
        pygame.draw.rect(s, self.cor, (7, 13, 24, 9), border_radius=4)

        # linha de destaque do corpo (dá leveza)
        pygame.draw.line(s, _aclarar(self.cor, 0.35), (10, 15), (26, 15), 1)

        # cabine (canopy)
        pygame.draw.ellipse(s, (170, 215, 255), (20, 15, 8, 5))

        # bico pontudo voltado para a direita
        pygame.draw.polygon(s, _aclarar(self.cor, 0.2),
                            [(27, 14), (33, 18), (27, 21)])
        pygame.draw.circle(s, (240, 250, 255), (32, 18), 1)

        # luzes policiais traseiras
        pygame.draw.circle(s, (255, 60, 60), (9, 14), 2)
        pygame.draw.circle(s, (80, 130, 255), (9, 20), 2)
        # escape traseiro
        pygame.draw.rect(s, (120, 130, 145), (5, 17, 2, 1))

    def _disparar_bala(self):
        tiro = Tiro(self.rect.centerx, self.rect.bottom,
                    0, VEL_RAJADA, cor=COR_RAJADA,
                    tamanho=VEL_RAJADA_TAMANHO)
        self._registrar_tiro(tiro)
        tocar("tiro_viatura")

    def _iniciar_rajada(self):
        self.tiros_rajada = QTD_RAJADA_VIATURA

    def update(self):
        self._movimentar()
        self._aplicar_tremor()
        # espelha o desenho de acordo com o sentido do movimento
        espelhar = self.velocidade_x < 0
        if espelhar != self._virado:
            self._virado = espelhar
            self.base_image = pygame.transform.flip(self.base_image, True, False)
        self._atualizar_visual()
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
        self.inclinacao_max = 5
        self.recuo = 0

    def _movimentar(self):
        self.rect.y += self.velocidade
        # movimento pesado: pequena oscilação lenta
        self.rect.y += math.sin(self.timer * 0.06) * 0.5
        if self.jogador is not None:
            if self.rect.centerx < self.jogador.rect.centerx:
                self.rect.x += 1
            elif self.rect.centerx > self.jogador.rect.centerx:
                self.rect.x -= 1

    def _desenhar(self):
        """Blindado pesado: esteiras largas, placas de armadura e canhão."""
        s = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image = s
        _sombra_oval(s, 4, 40, 42, 7)

        # esteiras laterais (largas, com frisos)
        for x in (6, 35):
            pygame.draw.rect(s, (52, 58, 74), (x, 9, 9, 32), border_radius=4)
            pygame.draw.rect(s, (30, 34, 46), (x, 9, 9, 32), 1, border_radius=4)
            pygame.draw.line(s, (70, 76, 92), (x + 2, 12), (x + 2, 39), 1)
            pygame.draw.line(s, (70, 76, 92), (x + 6, 12), (x + 6, 39), 1)

        # casco principal
        pygame.draw.rect(s, _escurecer(self.cor, 0.7), (10, 7, 30, 38),
                         border_radius=5)
        pygame.draw.rect(s, self.cor, (11, 8, 28, 36), border_radius=4)

        # placa de blindagem superior (decks sobrepostos)
        pygame.draw.rect(s, _aclarar(self.cor, 0.35), (14, 11, 22, 14),
                         border_radius=3)
        pygame.draw.rect(s, _escurecer(self.cor, 0.6), (14, 11, 22, 14), 1,
                         border_radius=3)
        for y in (13, 18):
            pygame.draw.line(s, (25, 20, 40), (16, y), (34, y), 1)

        # reforço frontal (frente ao jogador)
        pygame.draw.rect(s, _aclarar(self.cor, 0.45), (14, 28, 22, 8),
                         border_radius=2)
        pygame.draw.rect(s, _escurecer(self.cor, 0.6), (14, 28, 22, 8), 1,
                         border_radius=2)
        pygame.draw.rect(s, (20, 20, 40), (18, 30, 14, 2))  # fresta de visão

        # rebites nas placas
        for (x, y) in ((16, 16), (30, 16), (16, 21), (30, 21)):
            pygame.draw.circle(s, (30, 15, 60), (x, y), 1)

        # faróis dianteiros
        pygame.draw.rect(s, (255, 250, 200), (14, 40, 3, 2))
        pygame.draw.rect(s, (255, 250, 200), (33, 40, 3, 2))

        # canhão frontal (sobe levemente durante o recuo)
        recuo = getattr(self, "recuo", 0)
        pygame.draw.rect(s, (40, 44, 54), (21, 38 - recuo, 8, 11))
        pygame.draw.rect(s, (52, 58, 70), (21, 38 - recuo, 8, 3))  # destaque
        pygame.draw.rect(s, (28, 30, 38), (20, 48 - recuo, 10, 2))  # boca

    def atirar(self):
        # bomba lenta, grande, explode ao tocar o jogador ou na base
        self.ativar_tremor(8)   # pequena vibração ao lançar a bomba
        self.recuo = 3          # recuo visual do canhão
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
        tocar("tiro_guarda_pesado")

    def update(self):
        self._movimentar()
        self._atualizar_visual()
        self.saiu_da_tela()
        self._aplicar_tremor()
        if self.recuo > 0:
            self.recuo -= 1
            self._desenhar()
            self.image = escalar(self.image, FATOR_ESCALA_INIMIGO)
            self.base_image = self.image.copy()
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
        self.inclinacao_max = 8
        # timers dos padrões específicos da fase 2
        self.timer_leque = 0
        self.intervalo_leque = INTERVALO_LEQUE_BOSS
        self.timer_bomba = 0
        self.intervalo_bomba = INTERVALO_BOMBA_BOSS
        self.timer_chamada = 0
        # entrada dramática: começa fora da tela e desce até o alto
        self.rect.centery = -90
        self.timer_entrada = 80
        self.blink_timer = 0

    def _movimentar(self):
        self.rect.x += self.direcao * self.velocidade
        # presença: balanço sutil enquanto patrulha
        self.rect.y += math.sin(self.timer * 0.06) * 0.5
        if self.rect.x <= 20 or self.rect.x >= LARGURA - self.rect.width:
            self.direcao *= -1

    def _desenhar(self):
        """Blindado policial pesado: casco, asas, cockpit, armas e cauda."""
        cor = COR_CHEFE_FASE2 if self.esta_na_fase2 else self.cor
        s = pygame.Surface((70, 70), pygame.SRCALPHA)
        self.image = s
        _sombra_oval(s, 5, 56, 60, 9, alpha=80)

        # asas varridas (para os lados, reforçando a silhueta)
        pygame.draw.polygon(s, _escurecer(cor, 0.7),
                            [(15, 14), (1, 22), (3, 34), (16, 40)])
        pygame.draw.polygon(s, _escurecer(cor, 0.7),
                            [(55, 14), (69, 22), (67, 34), (54, 40)])
        pygame.draw.line(s, _aclarar(cor, 0.2), (4, 28), (15, 38), 2)
        pygame.draw.line(s, _aclarar(cor, 0.2), (66, 28), (55, 38), 2)

        # boom da cauda (traseira) + lemes
        pygame.draw.rect(s, (70, 74, 84), (28, 3, 14, 16), border_radius=4)
        pygame.draw.rect(s, (48, 52, 62), (28, 3, 14, 16), 1, border_radius=4)
        for x in (28, 42):
            pygame.draw.polygon(s, (58, 62, 72),
                                [(x, 4), (x - 3, 1), (x + 1, 3)])
            pygame.draw.polygon(s, (58, 62, 72),
                                [(x, 17), (x - 3, 20), (x + 1, 18)])
        pygame.draw.rect(s, (110, 120, 135), (31, 4, 8, 6))  # motor
        pygame.draw.circle(s, (255, 140, 40), (35, 12), 4)   # exaustão

        # casco principal
        pygame.draw.rect(s, _escurecer(cor, 0.7), (12, 14, 46, 40),
                         border_radius=10)
        pygame.draw.rect(s, cor, (13, 15, 44, 38), border_radius=9)

        # painel central com linha de detalhe
        pygame.draw.rect(s, _escurecer(cor, 0.85), (18, 18, 34, 14),
                         border_radius=4)
        pygame.draw.line(s, _aclarar(cor, 0.25), (18, 21), (52, 21), 1)

        # blindagem frontal extra
        pygame.draw.rect(s, _escurecer(cor, 0.6), (18, 40, 34, 8),
                         border_radius=3)
        # cockpit (vidro dianteiro, frente ao jogador)
        pygame.draw.rect(s, (160, 205, 240), (20, 44, 30, 8), border_radius=3)
        pygame.draw.line(s, (120, 170, 210), (28, 44), (28, 52), 1)
        pygame.draw.line(s, (120, 170, 210), (42, 44), (42, 52), 1)

        # nariz pontudo (em direção ao jogador)
        pygame.draw.polygon(s, _escurecer(cor, 0.85),
                            [(24, 48), (46, 48), (35, 62)])
        pygame.draw.polygon(s, _aclarar(cor, 0.12),
                            [(26, 49), (44, 49), (35, 60)])

        # pods de mísseis nas asas
        pygame.draw.rect(s, (52, 58, 70), (6, 30, 7, 12), border_radius=2)
        pygame.draw.rect(s, (52, 58, 70), (57, 30, 7, 12), border_radius=2)
        pygame.draw.circle(s, (20, 22, 30), (9, 34), 1)
        pygame.draw.circle(s, (20, 22, 30), (61, 34), 1)

        # fixações mecânicas (rebites)
        for (x, y) in ((18, 28), (34, 28), (50, 28), (18, 38), (34, 38),
                       (50, 38)):
            pygame.draw.circle(s, _escurecer(cor, 0.6), (x, y), 1)

        # faróis dianteiros
        pygame.draw.circle(s, (255, 250, 200), (23, 50), 2)
        pygame.draw.circle(s, (255, 250, 200), (47, 50), 2)

        # rachaduras de dano intenso (fase 2)
        if self.esta_na_fase2:
            pygame.draw.lines(s, (120, 10, 10), False,
                              [(30, 20), (34, 26), (31, 34), (38, 40)], 2)
            pygame.draw.lines(s, (120, 10, 10), False,
                              [(44, 24), (41, 30), (47, 36)], 2)

    def _desenhar_luzes(self):
        """Barra policial piscando + brilho do motor (animação leve).

        Desenhado sobre um overlay na escala original e redimensionado para
        acompanhar o tamanho (e a inclinação) da imagem atual.
        """
        fase = (self.timer // 16) % 2
        vermelho = (255, 70, 70) if fase == 0 else (150, 30, 30)
        azul = (80, 130, 255) if fase == 0 else (35, 55, 140)

        overlay = pygame.Surface((70, 70), pygame.SRCALPHA)
        # barra de luzes policiais na frente do cockpit
        pygame.draw.rect(overlay, (25, 28, 55), (20, 34, 30, 5),
                         border_radius=2)
        for cx in (24, 31, 40, 47):
            cor_luz = vermelho if cx in (24, 40) else azul
            pygame.draw.circle(overlay, cor_luz, (cx, 37), 3)

        # pulso do motor traseiro
        raio = 3 + int(math.sin(self.timer * 0.25))
        pygame.draw.circle(overlay, (255, 120, 40), (35, 11), raio)
        pygame.draw.circle(overlay, (255, 200, 100), (35, 11),
                           max(2, raio - 1))

        overlay = redimensionar(overlay, *self.image.get_size())
        self.image.blit(overlay, (0, 0))

    def tomar_dano(self, dano):
        """Chefe pisca de branco ao receber dano (reação)."""
        super().tomar_dano(dano)
        self.blink_timer = 4

    def entrar_fase2(self):
        if not self.esta_na_fase2:
            self.esta_na_fase2 = True
            self.velocidade = self.velocidade + 2
            self.intervalo_tiro = 35
            self._desenhar()
            self.image = escalar(self.image, FATOR_ESCALA_INIMIGO)
            self.base_image = self.image.copy()
            tocar("boss_fase2")
            # explosão visual de fragmentos + flash na mudança de fase
            if self.todos_sprites is not None:
                flash = Flash(self.rect.centerx, self.rect.centery,
                              (255, 90, 30), raio_max=34, duracao=16)
                self.todos_sprites.add(flash)
                for _ in range(18):
                    ang = random.uniform(0, math.tau)
                    vel = random.uniform(1, 5)
                    p = Particula(
                        self.rect.centerx, self.rect.centery,
                        math.cos(ang) * vel, math.sin(ang) * vel - 1,
                        COR_CHEFE_FASE2, tamanho=random.randint(2, 5),
                        duracao=random.randint(14, 24), gravidade=0.06,
                    )
                    self.todos_sprites.add(p)

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
        tocar("tiro_boss")

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
        tocar("tiro_viatura")

    def _bomba_especial(self):
        tiro = Tiro(self.rect.centerx, self.rect.bottom,
                    0, VEL_BOMBA_BOSS, cor=COR_BOMBA_BOSS,
                    tamanho=VEL_BOMBA_BOSS_TAMANHO,
                    homing=self.jogador,
                    raio_explosao=RAIO_EXPLOSAO_BOMBA_BOSS,
                    cor_explosao=COR_EXPLOSAO_BOMBA_BOSS,
                    explodir_na_linha=LINHA_EXPLOSAO_BOMBA)
        self._novo_tiro(tiro)
        tocar("tiro_guarda_pesado")

    def chamar_guardas(self):
        if self.grupo_inimigos is None:
            return
        for _ in range(2):
            guarda = Guarda(
                random.randint(40, LARGURA - 40), -40, self.jogador
            )
            self.grupo_inimigos.add(guarda)

    def update(self):
        self._aplicar_tremor()

        # entrada dramática: desce do topo sem atacar
        if self.timer_entrada > 0:
            self.timer_entrada -= 1
            self.timer += 1
            self.image = self.base_image.copy()
            self._desenhar_luzes()
            if self.rect.centery >= 70:
                self.rect.centery = 70
                self.timer_entrada = 0
            else:
                self.rect.y += 4
            self._aplicar_tremor()
            return

        self._movimentar()
        self._atualizar_visual()
        self._desenhar_luzes()

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

        # resposta visual ao receber dano (piscar branco)
        if self.blink_timer > 0:
            self.blink_timer -= 1
            frame = self.image.convert_alpha()
            overlay = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 110))
            frame.blit(overlay, (0, 0))
            self.image = frame
