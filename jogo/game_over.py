"""
Classe GameOver: tela de fim de jogo com pontuação e opções.
"""
import random
import pygame
from .settings import (
    LARGURA, ALTURA,
    COR_MENU_FUNDO, COR_ROBO, COR_MENU_TEXTO,
    COR_MENU_DESTAQUE, COR_MENU_SOMBRA
)


class GameOver:
    def __init__(self, pontos):
        self.pontos = pontos
        self.fonte_titulo = pygame.font.SysFont(None, 90)
        self.fonte_texto = pygame.font.SysFont(None, 40)
        self.fonte_pequena = pygame.font.SysFont(None, 30)

        self.timer = 0
        self.visivel = True

        self.particulas = []
        for _ in range(60):
            x = random.randint(0, LARGURA)
            y = random.randint(0, ALTURA)
            velocidade = random.uniform(0.3, 1.2)
            tamanho = random.randint(1, 3)
            self.particulas.append([x, y, velocidade, tamanho])

    def atualizar(self):
        self.timer += 1
        if self.timer % 25 == 0:
            self.visivel = not self.visivel

        for p in self.particulas:
            p[1] += p[2]
            if p[1] > ALTURA:
                p[1] = 0
                p[0] = random.randint(0, LARGURA)

    def desenhar(self, tela):
        tela.fill(COR_MENU_FUNDO)

        for p in self.particulas:
            brilho = int(80 + p[2] * 60)
            cor = (brilho, brilho // 4, brilho // 4)
            pygame.draw.circle(tela, cor, (int(p[0]), int(p[1])), p[3])

        titulo = self.fonte_titulo.render("GAME OVER", True, COR_ROBO)
        sombra = self.fonte_titulo.render("GAME OVER", True, COR_MENU_SOMBRA)
        tela.blit(sombra, (LARGURA // 2 - titulo.get_width() // 2 + 4, 134))
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 130))

        pontos_texto = self.fonte_texto.render(
            f"Pontuacao Final: {self.pontos}", True, COR_MENU_DESTAQUE
        )
        tela.blit(
            pontos_texto,
            (LARGURA // 2 - pontos_texto.get_width() // 2, 260)
        )

        if self.visivel:
            reiniciar = self.fonte_texto.render(
                "ENTER - Reiniciar", True, COR_MENU_DESTAQUE
            )
            tela.blit(
                reiniciar,
                (LARGURA // 2 - reiniciar.get_width() // 2, 380)
            )

        sair = self.fonte_texto.render(
            "ESC - Sair", True, COR_MENU_TEXTO
        )
        tela.blit(
            sair,
            (LARGURA // 2 - sair.get_width() // 2, 440)
        )

        dica = self.fonte_pequena.render(
            "Obrigado por jogar!", True, COR_MENU_TEXTO
        )
        tela.blit(
            dica,
            (LARGURA // 2 - dica.get_width() // 2, 520)
        )

    def tratar_evento(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "reiniciar"
            if event.key == pygame.K_ESCAPE:
                return "sair"
        return None
