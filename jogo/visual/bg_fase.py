"""
Background da gameplay: cidade inspirada em Nova York vista de cima.

Tudo é desenhado proceduralmente com formas do Pygame, num "tile" que se
repete verticalmente. O tile é rolado de cima para baixo para dar a
sensação de que o avião está avançando sobre a cidade.

Prioridade visual: JOGADOR > INIMIGOS > PROJÉTEIS > BACKGROUND.
Por isso prédios e ruas usam cores discretas (pouco saturadas).
"""
import random

import pygame

from ..settings import (
    LARGURA, ALTURA,
    COR_CIDADE_FUNDO, COR_RUA, COR_AVENIDA, COR_FAIXA_RUA, COR_ZEBRA,
    COR_PREDIO_1, COR_PREDIO_2, COR_PREDIO_3, COR_PREDIO_4,
    COR_PREDIO_BORDA, COR_PARQUE, COR_PARQUE_BORDA, COR_ARVORE,
    COR_ESTACIONAMENTO, COR_CARRO,
)

# Passo vertical das ruas (fileiras de quarteirões)
PASSO_V = 150
# Altura do tile: múltiplo de PASSO_V e >= 2 telas, para o loop ser contínuo
TILE_H = ((ALTURA * 3 + PASSO_V - 1) // PASSO_V) * PASSO_V
# Avenidas verticais (posição dos eixos centrais)
AVENIDAS = [220, 640, 1060]
# Limites dos quarteirões no eixo x (bordas da tela + avenidas)
COLUNAS = [0, 220, 640, 1060, LARGURA]
RUA_H = 16
AVENIDA_L = 24

CORES_PREDIO = [COR_PREDIO_1, COR_PREDIO_2, COR_PREDIO_3, COR_PREDIO_4]

# Divisor usado no desfoque do cenário (quanto maior, mais desfocado,
# dando a impressão de que o avião está mais alto)
DESFOQUE_CENARIO = 6

# Nuvens ocasionais entre o chão e o avião (sensação de altitude variável)
NUVEM_INTERVALO_MIN = 180          # frames entre nuvens
NUVEM_INTERVALO_MAX = 420


def _escurecer(cor, fator=0.55):
    return tuple(max(0, min(255, int(c * fator))) for c in cor)


class BackgroundFase:
    def __init__(self):
        self.vel_base = 1.6          # rolagem em px por frame (jogador parado)
        self.offset = 0.0
        self.tile = self._desfocar(self._gerar_tile())
        self.carros = self._gerar_carros()
        self.nuvens = []
        self.timer_nuvem = random.randint(60, 150)

    @staticmethod
    def _desfocar(superficie):
        """Aplica um desfoque visível (downscale + upscale suavizado)."""
        w, h = superficie.get_size()
        pequeno = pygame.transform.smoothscale(
            superficie,
            (max(1, w // DESFOQUE_CENARIO), max(1, h // DESFOQUE_CENARIO)))
        return pygame.transform.smoothscale(pequeno, (w, h))

    # ------------------------------------------------------------------
    # Geração do cenário (feita uma única vez na criação)
    # ------------------------------------------------------------------
    def _gerar_tile(self):
        tile = pygame.Surface((LARGURA, TILE_H), pygame.SRCALPHA)
        tile.fill(COR_CIDADE_FUNDO)

        # ruas horizontais (malha urbana)
        for r in range(TILE_H // PASSO_V):
            y = r * PASSO_V
            pygame.draw.rect(tile, COR_RUA, (0, y - RUA_H // 2, LARGURA, RUA_H))
            self._faixa_central(tile, y, horizontal=True)
        # avenidas verticais (mais largas)
        for ax in AVENIDAS:
            pygame.draw.rect(tile, COR_AVENIDA,
                             (ax - AVENIDA_L // 2, 0, AVENIDA_L, TILE_H))
            for r in range(TILE_H // PASSO_V):
                self._faixa_central(tile, r * PASSO_V, horizontal=False,
                                    eixo=ax)
        # faixas de pedestre nos cruzamentos das avenidas
        for ax in AVENIDAS:
            for r in range(1, TILE_H // PASSO_V):
                y = r * PASSO_V
                pygame.draw.rect(tile, COR_ZEBRA, (ax - AVENIDA_L // 2 - 8,
                                                   y - 5, 5, 10))
                pygame.draw.rect(tile, COR_ZEBRA, (ax + AVENIDA_L // 2 + 3,
                                                   y - 5, 5, 10))
        # quarteirões (prédios, parques, estacionamentos)
        self._desenhar_quarteiroes(tile)
        return tile

    @staticmethod
    def _faixa_central(tile, y, horizontal, eixo=None):
        """Faixa tracejada (amarela) no centro da pista."""
        if horizontal:
            passo = 30
            for x in range(10, LARGURA, passo):
                pygame.draw.rect(tile, COR_FAIXA_RUA, (x, y - 2, 16, 3))
        else:
            for yf in range(10, TILE_H, 30):
                pygame.draw.rect(tile, COR_FAIXA_RUA,
                                 (eixo - 2, yf, 3, 16))

    def _desenhar_quarteiroes(self, tile):
        for r in range(TILE_H // PASSO_V):
            y0 = r * PASSO_V + 10
            y1 = (r + 1) * PASSO_V - 10
            for c in range(len(COLUNAS) - 1):
                x0 = COLUNAS[c] + 14
                x1 = COLUNAS[c + 1] - 14
                if x1 - x0 < 30:
                    continue
                # parque grande (estilo Central Park) na coluna da direita
                if c == 3 and 3 <= r <= 8:
                    self._parque(tile, x0, x1, y0, y1)
                    continue
                chance = random.random()
                if chance < 0.08:
                    self._parque(tile, x0, x1, y0, y1)
                elif chance < 0.16:
                    self._estacionamento(tile, x0, x1, y0, y1)
                else:
                    self._edificios(tile, x0, x1, y0, y1)

    def _edificios(self, tile, x0, x1, y0, y1):
        """Prédios de topo (retângulos cartoon) dentro de um quarteirão."""
        n = random.choice([1, 1, 2, 2])
        largura = x1 - x0
        folga = 8 if n == 1 else 4
        larg_b = (largura - folga * (n - 1)) // n
        x = x0
        for i in range(n):
            if i == n - 1:
                larg_b = x1 - x
            cor = random.choice(CORES_PREDIO)
            borda = COR_PREDIO_BORDA
            # prédio ocupa quase toda a altura, alguns deixam uma 'sobra'
            y_inicio = y0 if random.random() < 0.7 else y0 + 18
            predio = pygame.Rect(x, y_inicio, larg_b, y1 - y_inicio)
            # sombra translúcida (profundidade)
            pygame.draw.rect(tile, (0, 0, 0, 60), predio.move(5, 6))
            pygame.draw.rect(tile, cor, predio)
            pygame.draw.rect(tile, borda, predio, 2)
            # parapeito do telhado (linha clara interna no topo)
            pygame.draw.line(tile, _escurecer(cor, 1.25),
                             (predio.x + 4, predio.y + 4),
                             (predio.right - 4, predio.y + 4), 2)
            x += larg_b + folga

    def _parque(self, tile, x0, x1, y0, y1):
        rect = pygame.Rect(x0, y0, x1 - x0, y1 - y0)
        pygame.draw.rect(tile, COR_PARQUE, rect, border_radius=8)
        pygame.draw.rect(tile, COR_PARQUE_BORDA, rect, 2, border_radius=8)
        arvores = max(1, ((x1 - x0) * (y1 - y0)) // 3500)
        for _ in range(arvores):
            ax_ = random.randint(x0 + 10, x1 - 10)
            ay_ = random.randint(y0 + 10, y1 - 10)
            pygame.draw.circle(tile, COR_ARVORE, (ax_, ay_), 5)

    def _estacionamento(self, tile, x0, x1, y0, y1):
        rect = pygame.Rect(x0, y0, x1 - x0, y1 - y0)
        pygame.draw.rect(tile, COR_ESTACIONAMENTO, rect)
        pygame.draw.rect(tile, _escurecer(COR_ESTACIONAMENTO, 1.3),
                         rect, 2)
        for x in range(x0 + 10, x1 - 6, 24):
            pygame.draw.line(tile, (96, 100, 104), (x, y0 + 5),
                             (x, y1 - 5), 1)

    def _gerar_carros(self):
        carros = []
        linhas = TILE_H // PASSO_V
        # carros nas ruas horizontais (poucos e discretos)
        for r in range(linhas):
            if random.random() < 0.3:
                n = random.randint(1, 2)
                for _ in range(n):
                    carros.append({
                        "x": random.uniform(10, LARGURA - 14),
                        "y": r * PASSO_V + random.choice([-5, 5]),
                        "dir": random.choice([-1, 1]),
                        "vel": random.uniform(0.9, 1.7),
                        "hor": True,
                        "cor": random.choice(COR_CARRO),
                    })
        # carros nas avenidas verticais
        for ax in AVENIDAS:
            for _ in range(1):
                carros.append({
                    "x": ax + random.choice([-7, 7]),
                    "y": random.uniform(20, TILE_H - 20),
                    "dir": random.choice([-1, 1]),
                    "vel": random.uniform(0.9, 1.7),
                    "hor": False,
                    "cor": random.choice(COR_CARRO),
                })
        return carros

    def _gerar_nuvem(self):
        """Cria uma nuvem em posição aleatória, vinda de cima da tela."""
        largura = random.randint(70, 150)
        altura = random.randint(28, 48)
        return {
            "surf": self._criar_nuvem(largura, altura),
            "x": random.uniform(-30, LARGURA - 30),
            "y": -altura - random.uniform(0, 120),
            "vx": random.uniform(-0.35, 0.35),
            # desce mais devagar que o chão (parallax por altitude)
            "vy": self.vel_base * random.uniform(0.2, 0.45),
        }

    @staticmethod
    def _criar_nuvem(largura, altura):
        """Nuvem translúcida e fofa, feita de círculos sobrepostos."""
        nuvem = pygame.Surface((largura, altura), pygame.SRCALPHA)
        branco = (255, 255, 255, random.randint(90, 150))
        centro = altura // 2
        for fx in (0.15, 0.35, 0.55, 0.75, 0.9):
            raio = random.randint(altura // 5, altura // 3)
            pygame.draw.circle(nuvem, branco,
                               (int(largura * fx), centro), raio)
        base = pygame.Rect(0, centro - altura // 4, largura, altura // 2)
        pygame.draw.ellipse(nuvem, branco, base)
        return nuvem

    # ------------------------------------------------------------------
    # Atualização e desenho
    # ------------------------------------------------------------------
    def atualizar(self, mult=1.0):
        """Rola o cenário para baixo. `mult` acelera junto com o jogador."""
        self.offset += self.vel_base * mult
        for carro in self.carros:
            if carro["hor"]:
                carro["x"] += carro["dir"] * carro["vel"]
                if carro["x"] > LARGURA + 10:
                    carro["x"] = -10
                elif carro["x"] < -10:
                    carro["x"] = LARGURA + 10
            else:
                carro["y"] += carro["dir"] * carro["vel"]
                carro["y"] %= TILE_H
        self._atualizar_nuvens(mult)

    def _atualizar_nuvens(self, mult):
        self.timer_nuvem -= 1
        if self.timer_nuvem <= 0:
            self.nuvens.append(self._gerar_nuvem())
            self.timer_nuvem = random.randint(NUVEM_INTERVALO_MIN,
                                              NUVEM_INTERVALO_MAX)
        for nuvem in self.nuvens:
            nuvem["x"] += nuvem["vx"]
            nuvem["y"] += nuvem["vy"] * mult
        self.nuvens = [n for n in self.nuvens if n["y"] < ALTURA + 40]

    @staticmethod
    def _desenhar_carro(tela, carro, y_base):
        if carro["hor"]:
            rect = pygame.Rect(int(carro["x"]), int(carro["y"]) + y_base,
                               10, 5)
        else:
            rect = pygame.Rect(int(carro["x"]), int(carro["y"]) + y_base,
                               5, 10)
        pygame.draw.rect(tela, _escurecer(carro["cor"], 0.6),
                         rect.move(1, 1))
        pygame.draw.rect(tela, carro["cor"], rect)
        # superfície clara (teto) para o carrinho
        inter = rect.inflate(-3, -3)
        pygame.draw.rect(tela, _escurecer(carro["cor"], 1.3), inter, 1)

    def desenhar(self, tela):
        # o cenário desce na tela, como se o avião avançasse sobre a cidade
        ciclo = self.offset % TILE_H
        y1 = int(ciclo)
        tela.blit(self.tile, (0, y1 - TILE_H))
        tela.blit(self.tile, (0, y1))
        for carro in self.carros:
            self._desenhar_carro(tela, carro, y1 - TILE_H)
            self._desenhar_carro(tela, carro, y1)
        # nuvens em altitudes variadas (desenham por cima da cidade)
        for nuvem in self.nuvens:
            tela.blit(nuvem["surf"], (int(nuvem["x"]), int(nuvem["y"])))