"""
Classe Menu: tela inicial do jogo com efeitos visuais.
"""
import random
import pygame
from .settings import (
    LARGURA, ALTURA,
    COR_MENU_FUNDO, COR_MENU_TITULO, COR_MENU_TEXTO,
    COR_MENU_DESTAQUE, COR_MENU_SOMBRA
)


class Menu:
    def __init__(self):
        self.fonte_titulo = pygame.font.SysFont(None, 80)
        self.fonte_texto = pygame.font.SysFont(None, 36)
        self.fonte_pequena = pygame.font.SysFont(None, 28)

        self.timer = 0
        self.visivel = True

        self.particulas = []
        for _ in range(80):
            x = random.randint(0, LARGURA)
            y = random.randint(0, ALTURA)
            velocidade = random.uniform(0.2, 1.0)
            tamanho = random.randint(1, 3)
            self.particulas.append([x, y, velocidade, tamanho])

    def atualizar(self):
        self.timer += 1
        if self.timer % 30 == 0:
            self.visivel = not self.visivel

        for p in self.particulas:
            p[1] += p[2]
            if p[1] > ALTURA:
                p[1] = 0
                p[0] = random.randint(0, LARGURA)

    def desenhar(self, tela):
        tela.fill(COR_MENU_FUNDO)

        for p in self.particulas:
            brilho = int(100 + p[2] * 100)
            cor = (brilho, brilho, brilho)
            pygame.draw.circle(tela, cor, (int(p[0]), int(p[1])), p[3])

        titulo = self.fonte_titulo.render("MACACUQUITO", True, COR_MENU_TITULO)
        sombra = self.fonte_titulo.render("MACACUQUITO", True, COR_MENU_SOMBRA)
        tela.blit(sombra, (LARGURA // 2 - titulo.get_width() // 2 + 3, 123))
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 120))

        louco = self.fonte_titulo.render("LOUCO", True, COR_MENU_DESTAQUE)
        sombra_louco = self.fonte_titulo.render("LOUCO", True, COR_MENU_SOMBRA)
        tela.blit(sombra_louco, (LARGURA // 2 - louco.get_width() // 2 + 3, 203))
        tela.blit(louco, (LARGURA // 2 - louco.get_width() // 2, 200))

        controles = [
            "CONTROLES:",
            "W A S D - Mover",
            "ESPACIO - Atirar",
        ]
        y = 300
        for linha in controles:
            texto = self.fonte_texto.render(linha, True, COR_MENU_TEXTO)
            tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, y))
            y += 35

        if self.visivel:
            iniciar = self.fonte_texto.render(
                "Pressione ENTER para jogar", True, COR_MENU_DESTAQUE
            )
            tela.blit(iniciar, (LARGURA // 2 - iniciar.get_width() // 2, 450))

        sair = self.fonte_pequena.render("ESC para sair", True, COR_MENU_TEXTO)
        tela.blit(sair, (LARGURA // 2 - sair.get_width() // 2, 520))

    def tratar_evento(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "iniciar"
            if event.key == pygame.K_ESCAPE:
                return "sair"
        return None
