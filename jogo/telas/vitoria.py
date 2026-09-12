"""
Classe Vitoria: tela exibida ao derrotar o chefe final.

Mostra a mensagem de missão concluída, o avião-banana e os macacos
comemorando, as estatísticas finais da partida e botões para jogar
novamente ou voltar ao menu principal.
"""
import math
import random

import pygame

from ..settings import (
    LARGURA, ALTURA,
    COR_MENU_DESTAQUE, COR_MENU_SOMBRA, COR_MENU_TEXTO, COR_MENU_TITULO,
    COR_SELVA_FUNDO, COR_BANANA, COR_MADEIRA, COR_MADEIRA_CLARA,
    COR_MADEIRA_BORDA, COR_MADEIRA_TEXTO,
)
from ..visual.tema import (
    desenhar_moldura_selva, desenhar_botao_selva, desenhar_macaco,
    banana_surface,
)
from ..entidades.jogador import _desenhar_aviao, _desenhar_helice
from ..sons import tocar


class Vitoria:
    def __init__(self, pontos, inimigos_derrotados, vidas):
        self.pontos = pontos
        self.inimigos_derrotados = inimigos_derrotados
        self.vidas = vidas

        self.fonte_titulo = pygame.font.SysFont(None, 64)
        self.fonte_subtitulo = pygame.font.SysFont(None, 34)
        self.fonte_painel = pygame.font.SysFont(None, 24)
        self.fonte_stats = pygame.font.SysFont(None, 28)
        self.fonte_botao = pygame.font.SysFont(None, 32)

        self.timer = 0
        self.botoes = []     # (rect, acao) desenhados no último frame
        self.hover_anterior = None

        # comemoração: confetes e bananas caindo nas laterais
        self.particulas = self._criar_particulas()
        self.bananas = self._criar_bananas()
        self.banana = banana_surface(12)

    # ------------------------------------------------------------------
    # Partículas de comemoração
    # ------------------------------------------------------------------
    def _criar_particulas(self):
        cores = [COR_BANANA, (255, 110, 150), (120, 200, 255),
                 (120, 220, 120), (255, 200, 40), (200, 120, 255)]
        particulas = []
        for _ in range(28):
            particulas.append({
                "x": random.uniform(0, LARGURA),
                "y": random.uniform(0, ALTURA),
                "vy": random.uniform(0.6, 1.6),
                "vx": random.uniform(-0.4, 0.4),
                "tamanho": random.randint(3, 6),
                "cor": random.choice(cores),
                "vida": random.uniform(40, 90),
            })
        return particulas

    def _criar_bananas(self):
        bananas = []
        for _ in range(7):
            lado = random.choice([-1, 1])
            if lado == -1:
                x_base = random.uniform(30, 180)
            else:
                x_base = random.uniform(LARGURA - 180, LARGURA - 30)
            bananas.append({
                "x": x_base,
                "y": random.uniform(-40, ALTURA),
                "vel": random.uniform(0.7, 1.3),
                "angulo": random.uniform(0, 360),
                "vel_ang": random.uniform(-2, 2),
            })
        return bananas

    def _atualizar_particulas(self):
        for p in self.particulas:
            p["y"] += p["vy"]
            p["x"] += p["vx"] + math.sin(self.timer * 0.05 + p["y"]) * 0.3
            p["vida"] -= 1
            if p["vida"] <= 0 or p["y"] > ALTURA + 10:
                p["x"] = random.uniform(0, LARGURA)
                p["y"] = random.uniform(-24, -5)
                p["vida"] = random.uniform(60, 120)
        for b in self.bananas:
            b["y"] += b["vel"]
            b["angulo"] += b["vel_ang"]
            if b["y"] > ALTURA + 30:
                b["y"] = random.uniform(-44, -10)

    # ------------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------------
    def atualizar(self):
        self.timer += 1
        self._atualizar_particulas()

    def desenhar(self, tela):
        tela.fill(COR_SELVA_FUNDO)
        desenhar_moldura_selva(tela, self.timer)

        self._desenhar_particulas(tela)
        self._desenhar_titulo(tela)
        self._desenhar_aviao(tela)
        self._desenhar_macacos(tela)
        self._desenhar_resultados(tela)
        self._desenhar_botoes(tela)

    # ------------------------------------------------------------------
    # Decoradores e mensagens
    # ------------------------------------------------------------------
    def _fade_in(self, inicio, duracao):
        """Alpha (0..255) de entrada suave a partir do frame `inicio`."""
        t = self.timer - inicio
        if t < 0:
            return 0
        if t >= duracao:
            return 255
        return int(255 * (t / duracao))

    def _desenhar_particulas(self, tela):
        for p in self.particulas:
            pygame.draw.rect(
                tela, p["cor"],
                (int(p["x"]), int(p["y"]), p["tamanho"], max(2, p["tamanho"] // 2)))
        for b in self.bananas:
            rot = pygame.transform.rotozoom(self.banana, b["angulo"], 1)
            tela.blit(rot, (int(b["x"] - rot.get_width() / 2),
                            int(b["y"] - rot.get_height() / 2)))

    def _desenhar_titulo(self, tela):
        alpha = self._fade_in(0, 18)
        cx = LARGURA // 2

        titulo = self.fonte_titulo.render(
            "OPERAÇÃO CONCLUÍDA!", True, COR_MENU_DESTAQUE)
        sombra = self.fonte_titulo.render(
            "OPERAÇÃO CONCLUÍDA!", True, COR_MENU_SOMBRA)

        # brilho discreto atrás do título
        brilho = pygame.Surface((titulo.get_width() + 80, 86),
                                pygame.SRCALPHA)
        pulsar = 22 + int(14 * math.sin(self.timer * 0.07))
        pygame.draw.ellipse(brilho, (255, 235, 120, pulsar),
                            brilho.get_rect())

        flut = int(math.sin(self.timer * 0.05) * 2)
        titulo.set_alpha(alpha)
        sombra.set_alpha(int(alpha * 0.5))
        brilho.set_alpha(alpha)

        tela.blit(brilho, (cx - brilho.get_width() // 2, 42))
        tela.blit(sombra, (cx - titulo.get_width() // 2 + 3, 52 + flut))
        tela.blit(titulo, (cx - titulo.get_width() // 2, 48 + flut))

        sub = self.fonte_subtitulo.render(
            "A BANANA ESTÁ SALVA!", True, COR_MENU_TEXTO)
        sub.set_alpha(self._fade_in(10, 20))
        tela.blit(sub, (cx - sub.get_width() // 2, 118))

    def _desenhar_aviao(self, tela):
        alpha = self._fade_in(16, 20)
        if alpha <= 0:
            return
        frame = pygame.Surface((46, 46), pygame.SRCALPHA)
        _desenhar_aviao(frame, "comemorar")
        _desenhar_helice(frame, self.timer * 2.2)

        aviao = pygame.transform.rotozoom(frame, 0, 2.0)
        aviao.set_alpha(alpha)
        cx = LARGURA // 2 + int(math.sin(self.timer * 0.04) * 6)
        cy = 250 + int(math.sin(self.timer * 0.07) * 4)
        tela.blit(aviao, (cx - aviao.get_width() // 2,
                          cy - aviao.get_height() // 2))

    def _desenhar_macacos(self, tela):
        # macacos dos dois lados, pequenos, comemorando
        desenhar_macaco(tela, 130, 400, self.timer,
                        olhar_x=LARGURA // 2, celebrar=True)
        desenhar_macaco(tela, LARGURA - 130, 400, self.timer,
                        olhar_x=LARGURA // 2, celebrar=True)

    def _desenhar_resultados(self, tela):
        alpha = self._fade_in(34, 20)
        if alpha <= 0:
            return
        cx = LARGURA // 2

        rect_painel = pygame.Rect(0, 0, 430, 120)
        rect_painel.center = (cx, 400)

        painel = pygame.Surface((430, 120), pygame.SRCALPHA)
        pygame.draw.rect(painel, (52, 36, 22), (4, 6, 426, 114),
                         border_radius=14)
        pygame.draw.rect(painel, COR_MADEIRA, rect_painel,
                         border_radius=14)
        pygame.draw.rect(painel, COR_MADEIRA_CLARA, rect_painel, 2,
                         border_radius=14)
        pygame.draw.rect(painel, COR_MADEIRA_BORDA, rect_painel, 4,
                         border_radius=14)
        painel.set_alpha(alpha)
        tela.blit(painel, rect_painel.topleft)

        cabecalho = self.fonte_painel.render(
            "RESULTADOS", True, COR_MADEIRA_TEXTO)
        cabecalho.set_alpha(alpha)
        tela.blit(cabecalho, (cx - cabecalho.get_width() // 2,
                              rect_painel.y + 11))

        linhas = [
            ("PONTUAÇÃO", f"{self.pontos}"),
            ("INIMIGOS", f"{self.inimigos_derrotados}"),
            ("VIDAS RESTANTES", f"{self.vidas}"),
        ]
        y = rect_painel.y + 45
        for rotulo, valor in linhas:
            text_r = self.fonte_stats.render(rotulo, True, COR_MENU_TEXTO)
            text_v = self.fonte_stats.render(valor, True, COR_MENU_DESTAQUE)
            text_r.set_alpha(alpha)
            text_v.set_alpha(alpha)
            tela.blit(text_r, (rect_painel.x + 30, y))
            tela.blit(text_v,
                      (rect_painel.right - text_v.get_width() - 30, y))
            y += 34

    def _desenhar_botoes(self, tela):
        mouse = pygame.mouse.get_pos()
        if self.timer >= 48:
            self._botao(tela, "JOGAR NOVAMENTE", self.fonte_botao, 578,
                        mouse, "reiniciar", largura=360, altura=60)
            self._botao(tela, "MENU PRINCIPAL", self.fonte_botao, 650,
                        mouse, "menu", largura=300, altura=50)

        acao_hover = None
        for rect, acao in self.botoes:
            if rect.collidepoint(mouse):
                acao_hover = acao
                break
        if acao_hover is not None and acao_hover != self.hover_anterior:
            tocar("menu_hover")
        self.hover_anterior = acao_hover

    def _botao(self, tela, texto, fonte, y, mouse, acao,
               largura=300, altura=56):
        rect = pygame.Rect(0, 0, largura, altura)
        rect.center = (LARGURA // 2, y)
        hover = rect.collidepoint(mouse)
        desenhar_botao_selva(
            tela, LARGURA // 2, y, largura, altura, texto,
            fonte, self.timer, hover)
        self.botoes.append((rect, acao))

    def tratar_evento(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, acao in self.botoes:
                if rect.collidepoint(event.pos):
                    return acao
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "reiniciar"
            if event.key == pygame.K_ESCAPE:
                return "menu"
        return None